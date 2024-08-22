
from datetime import date
import random

import pycountry
from db import get_db
from db.models import DailyCountry, Guess, Question
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select, or_
from db.models import User
from sqlalchemy.ext.asyncio import AsyncSession

from game.schemas import QuestionCreate, UserHistory


async def generate_new_country(session: AsyncSession):
    
    countries = list(pycountry.countries)
    selected_country = random.choice(countries)
    
    print(f"Type of selected country: {type(selected_country)}")    
    
    # Create a new country entry in the database
    new_country = await create_daily_country(session, selected_country.name)
    
    print(f"Generated new country for quiz: {selected_country.name}")
    return new_country

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
    entity = result.scalars().first()
    if entity is not None:
        return entity
    
    return await generate_new_country(session)
    
    
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

async def get_player_histiory_for_country(user: User, daily_country: DailyCountry, session: AsyncSession) -> UserHistory:
    questions_result = await session.execute(
        select(Question).where(Question.user_id == user.id, Question.country_id == daily_country.id)
    )
    questions = questions_result.scalars().all()

    # Query for guesses
    guesses_result = await session.execute(
        select(Guess).where(Guess.user_id == user.id, Guess.country_id == daily_country.id)
    )
    guesses = guesses_result.scalars().all()

    return UserHistory(
        user=user,
        questions=questions,
        guesses=guesses
    )
