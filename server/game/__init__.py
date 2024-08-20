import random
from fastapi import APIRouter, Depends, HTTPException, status
import pycountry

from db.models import User
import game.utils as gutils
from .schemas import GuessBase, GuessDisplay, QuestionDisplay
from db import get_db
from fastapi import APIRouter
import game.crud as gcrud
import users.crud as ucrud
from users.utils import oauth2_scheme, verify_access_token
from sqlalchemy.ext.asyncio import AsyncSession


async def generate_new_country():
    async with get_db() as db:
        countries = list(pycountry.countries)
        selected_country = random.choice(countries)
        
        print(f"Type of selected country: {type(selected_country)}")    
        
        # Create a new country entry in the database
        await gcrud.create_daily_country(db, selected_country.name)
    
    print(f"Generated new country for quiz: {selected_country.name}")
    
router = APIRouter()

@router.post("/guess", response_model=GuessDisplay)
async def get_game(guess: GuessBase, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    daily_country = await gcrud.get_today_country(db)
    username = verify_access_token(token)
    

    user: User = await ucrud.get_user(username, db)
    if not user:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    return await gutils.give_guess(
        guess=guess.guess, 
        daily_country=daily_country,
        user=user,
        session=db
    )


@router.post("/question", response_model=QuestionDisplay)
async def ask_question(question: str, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    daily_country = await gcrud.get_today_country(db)
    username = verify_access_token(token)
    
    user: User = await ucrud.get_user(username, db)
    if not user:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    return await gutils.ask_question(
        question=question, 
        daily_country=daily_country,
        user=user,
        db=db
    )