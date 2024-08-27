from db import get_db
from db.models import User
from db.repositories.countrydle import CountrydleRepository
from db.repositories.user import UserRepository
from db.schemas.countrydle import (
    GuessBase,
    GuessDisplay,
    QuestionBase,
    QuestionDisplay,
    UserHistory,
)
from dotenv import load_dotenv
from fastapi import APIRouter, Cookie, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from users.utils import verify_access_token

import countrydle.utils as gutils

load_dotenv()

router = APIRouter()


@router.post("/guess", response_model=GuessDisplay)
async def get_game(
    guess: GuessBase,
    access_token: str = Cookie(None),
    session: AsyncSession = Depends(get_db),
):
    daily_country = await CountrydleRepository(session).get_today_country()

    username = verify_access_token(access_token)
    user: User = await UserRepository(session).get_user(username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return await gutils.give_guess(
        guess=guess.guess, daily_country=daily_country, user=user, session=session
    )


@router.post("/question", response_model=QuestionDisplay)
async def ask_question(
    question: QuestionBase,
    access_token: str = Cookie(None),
    session: AsyncSession = Depends(get_db),
):
    daily_country = await CountrydleRepository(session).get_today_country()

    username = verify_access_token(access_token)
    user: User = await UserRepository(session).get_user(username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return await gutils.ask_question(
        question=question.question,
        day_country=daily_country,
        user=user,
        session=session,
    )


@router.get("/history", response_model=UserHistory)
async def my_hisotry(
    access_token: str = Cookie(None), session: AsyncSession = Depends(get_db)
):
    daily_country = await CountrydleRepository(session).get_today_country()

    username = verify_access_token(access_token)
    user: User = await UserRepository(session).get_user(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return await CountrydleRepository(session).get_player_histiory_for_today(
        user, daily_country
    )
