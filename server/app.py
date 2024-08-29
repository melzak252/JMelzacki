import asyncio
import datetime
import logging
from contextlib import asynccontextmanager

import users.crud as ucrud
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from countrydle import router as countrydle_router
from countrydle.crud import populate_countries
from db import AsyncSessionLocal, get_db, get_engine
from db.base import Base
from db.models import *  # noqa: F403
from db.repositories.countrydle import CountrydleRepository
from db.repositories.user import UserRepository
from db.schemas.user import UserCreate, UserDisplay
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from qdrant import close_qdrant_client, init_qdrant
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from users import router as users_router
from users.utils import create_access_token

load_dotenv()

scheduler = AsyncIOScheduler()


async def generate_country_for_today():
    async with AsyncSessionLocal() as session:
        await CountrydleRepository(session).generate_new_day_country()


scheduler.add_job(generate_country_for_today, CronTrigger(hour=0, minute=1))

async def init_models(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logging.info("Database connection established and models created.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = get_engine()
    try:
        await init_models(engine)
        scheduler.start()

        async with AsyncSessionLocal() as session:
            await ucrud.add_base_permissions(session)
            await populate_countries(session)
            await init_qdrant(session)

            c_repo = CountrydleRepository(session)
            if await c_repo.get_today_country() is None:
                await c_repo.generate_new_day_country()

        yield
    except ConnectionRefusedError:
        logging.error("Exiting application due to database connection failure.")
        await asyncio.sleep(10)
        raise
    except Exception as e:
        logging.error("Exiting application due to error.")
        raise e
    finally:
        try:
            logging.info("Shutting down application...")
            scheduler.shutdown(wait=True)
            close_qdrant_client()
            await engine.dispose()
            logging.info("Application shutdown complete.")
        except Exception as e:
            logging.error(f"Error during shutdown: {e}")


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(countrydle_router, tags=["countrydle"])


@app.get("/")
async def root():
    return {"message": "Welcome to the Game API!"}


@app.post("/login")
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db),
):
    user = await UserRepository(session).get_user(form_data.username)

    if not user or not UserRepository.verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user.username})

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,  # Set to True in production
        samesite="Lax",
        path="/",
    )
    return {
        "access_token": access_token,
        "username": user.username,
        "token_type": "bearer",
    }


@app.post("/logout", status_code=status.HTTP_200_OK)
async def logout(response: Response):
    response.set_cookie(
        key="access_token",
        value="",
        httponly=True,
        secure=True,  # Set to True in production
        expires=datetime.datetime.now().isoformat(),
        samesite="Lax",
        path="/",
    )
    return {"success": 1}


@app.post("/register", response_model=UserDisplay)
async def register(user: UserCreate, session: AsyncSession = Depends(get_db)):
    return await UserRepository(session).register_user(user=user)
