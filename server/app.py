
import asyncio
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
        CountrydleRepository(session).generate_new_day_country(session=session)


scheduler.add_job(generate_country_for_today, CronTrigger(hour=0, minute=1))

RETRY_LIMIT = 5  # Number of times to retry the connection
RETRY_DELAY = 5  # Seconds to wait before each retry


async def init_models(engine: AsyncEngine):
    retries = 0
    while retries < RETRY_LIMIT:
        logging.info(f"Database connecting {retries} try.")

        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logging.info("Database connection established and models created.")

            break
        except ConnectionRefusedError as e:
            retries += 1
            logging.warning(
                f"Database connection failed. Retrying {retries}/{RETRY_LIMIT}... Error: {e}"
            )
            await asyncio.sleep(RETRY_DELAY)
    else:
        logging.error("Could not connect to the database after multiple retries.")
        raise RuntimeError("Database initialization failed after multiple retries.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = get_engine()
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

    close_qdrant_client()
    scheduler.shutdown()
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Specify domains for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(countrydle_router, prefix="/cuntrydle", tags=["countrydle"])


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

    if not user or not UserRepository.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user.username})

    response.set_cookie(
        key="access_token",
        value=access_token,  # No 'Bearer' prefix needed
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


@app.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Successfully logged out"}


@app.post("/register", response_model=UserDisplay)
async def register(user: UserCreate, session: AsyncSession = Depends(get_db)):
    return await UserRepository(session).register_user(user=user)
