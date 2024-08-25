import random
from fastapi import APIRouter, Body, Cookie, Depends, HTTPException, status
import pycountry

from db.models import User
import countrydle.utils as gutils
from .schemas import GuessBase, GuessDisplay, QuestionBase, QuestionDisplay, UserHistory
from db import get_db
from fastapi import APIRouter
import countrydle.crud as gcrud
import users.crud as ucrud
from users.utils import oauth2_scheme, verify_access_token
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.post("/guess", response_model=GuessDisplay)
async def get_game(guess: GuessBase, access_token: str = Cookie(None), db: AsyncSession = Depends(get_db)):
    daily_country = await gcrud.get_today_country(db)
    username = verify_access_token(access_token)

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
async def ask_question(question: QuestionBase, access_token: str = Cookie(None), db: AsyncSession = Depends(get_db)):
    daily_country = await gcrud.get_today_country(db)
    username = verify_access_token(access_token)
    
    user: User = await ucrud.get_user(username, db)
    if not user:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    return await gutils.ask_question(
        question=question.question, 
        daily_country=daily_country,
        user=user,
        db=db
    )



@router.get("/history", response_model=UserHistory)
async def my_hisotry(access_token: str = Cookie(None), session: AsyncSession = Depends(get_db)):
    daily_country = await gcrud.get_today_country(session)
    if not access_token:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    username = verify_access_token(access_token)
    print(username)
    user: User = await ucrud.get_user(username, session)
    
    if not user:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    return await gcrud.get_player_histiory_for_today(user, daily_country, session)
    # return UserHistory(user=None,
    #                    questions=[],
    #                    guesses=[])