
from datetime import date
from db.models import DailyCountry, Guess, Question
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select, or_
from db.models import User
from sqlalchemy.ext.asyncio import AsyncSession

from game.schemas import QuestionCreate

async def create_daily_country(session: AsyncSession, country_name: str) -> DailyCountry:
    new_entry = DailyCountry(
        country_name=country_name
    )
    
    session.add(new_entry)

    try:
        await session.commit()  # Commit the transaction
        await session.refresh(new_entry)  # Refresh the instance to get the ID
    except Exception as ex:
        await session.rollback()
        raise ex
    
    return new_entry

async def get_today_country(session: AsyncSession) -> DailyCountry:
    result = await session.execute(
        select(DailyCountry).where(DailyCountry.date == date.today()).order_by(DailyCountry.id.desc())
    )
    return result.scalars().first()
    
async def create_question(question: str, answer: str, user_id: int, country_id: int, explanation: str, session: AsyncSession) -> Question:
    new_entry = Question(
        user_id =user_id,
        country_id = country_id,
        question = question,
        answer = answer,
        explanation = explanation
    )
    
    session.add(new_entry)

    try:
        await session.commit()  # Commit the transaction
        await session.refresh(new_entry)  # Refresh the instance to get the ID
    except Exception as ex:
        await session.rollback()
        raise ex
    
    return new_entry

async def create_guess(guess: str, answer: str, user_id: int, country_id: int, session: AsyncSession) -> Question:
    new_entry = Guess(
        user_id =user_id,
        country_id = country_id,
        guess = guess,
        response = answer
    )
    
    session.add(new_entry)

    try:
        await session.commit()  # Commit the transaction
        await session.refresh(new_entry)  # Refresh the instance to get the ID
    except Exception as ex:
        await session.rollback()
        raise ex
    
    return new_entry