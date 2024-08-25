from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordRequestForm

from countrydle.crud import generate_new_day_country, get_today_country, populate_countries
from users.schemas import UserCreate, UserDisplay

load_dotenv() 
from fastapi import Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from users.utils import create_access_token, oauth2_scheme, add_base_permissions
import users.crud as ucrud
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from sqlalchemy.ext.asyncio import AsyncEngine
from db import AsyncSessionLocal, get_db, get_engine
from db.base import Base
from db.models import *

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from users import router as users_router
from countrydle import router as countrydle_router
from sqlalchemy.ext.asyncio import AsyncEngine


scheduler = AsyncIOScheduler()
 
async def generate_country_for_today():   
    async with AsyncSessionLocal() as session:
        generate_new_day_country(session=session)
        
scheduler.add_job(generate_country_for_today, CronTrigger(hour=0, minute=1))

async def init_models(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = get_engine()
    await init_models(engine)
    scheduler.start()
    
    async with AsyncSessionLocal() as session:
        await add_base_permissions(session)
        await populate_countries(session)
        
        if await get_today_country(session) is None:
            await generate_new_day_country(session)
        
    yield
    
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
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user: User = await ucrud.get_user(form_data.username, db)
    
    if not user or not User.verify_password(form_data.password, user.hashed_password):
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
    return {"access_token": access_token, "username": user.username, "token_type": "bearer"}


@app.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Successfully logged out"}

@app.post("/register", response_model=UserDisplay)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await ucrud.register_user(user=user, session=db)