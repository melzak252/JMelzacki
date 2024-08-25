
from datetime import date
import random
import csv

import pycountry
from db.models import Country, DayCountry, Guess, Question
from sqlalchemy import select
from db.models import User
from sqlalchemy.ext.asyncio import AsyncSession

from countrydle.schemas import CountryBase, UserHistory


async def generate_new_day_country(session: AsyncSession):
    result = await session.execute(
        select(Country)
    )
    
    countries = result.scalars().all()
    if not countries:
        raise ValueError("No countries in database!")
    
    country = random.choice(countries)
    
    new_country = await create_day_country(session, country)
    
    print(f"Generated new country for quiz: {country.name}")
    return new_country

async def create_day_country(session: AsyncSession, country: Country) -> DayCountry:
    new_entry = DayCountry(
        country_id=country.id
    )
    
    
    session.add(new_entry)

    try:
        await session.commit()  # Commit the transaction
        await session.refresh(new_entry)  # Refresh the instance to get the ID
    except Exception as ex:
        await session.rollback()
        raise ex
    
    return new_entry

async def get_today_country(session: AsyncSession) -> DayCountry:
    result = await session.execute(
        select(DayCountry).where(DayCountry.date == date.today()).order_by(DayCountry.id.desc())
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

async def create_country(country: CountryBase, session: AsyncSession) -> Country:
    new_entry = Country(**country.model_dump())
    
    session.add(new_entry)

    try:
        await session.commit()  # Commit the transaction
        await session.refresh(new_entry)  # Refresh the instance to get the ID
    except Exception as ex:
        await session.rollback()
        raise ex
    
    return new_entry

async def get_player_histiory_for_today(user: User, daily_country: DayCountry, session: AsyncSession) -> UserHistory:
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

async def populate_countries(session: AsyncSession):
    result = await session.execute(
        select(Country)
    )
    
    countries = result.scalars().all()
    
    if countries:
        return
    
    with open("data/countries.csv", "r", encoding="utf8") as f:
        reader = csv.DictReader(f, fieldnames=["name", "official_name", "wiki_page"])
        next(reader)
        countries = [
            Country(
                name=row["name"],
                official_name=row["official_name"],
                wiki=row["wiki_page"],
                md_file=f"data/pages/{row['name']}.md"
            ) for row in reader
        ]
        print(len(countries))    
        session.add_all(countries)
        
        try:
            await session.commit()  # Commit the transaction
            
        except Exception as ex:
            await session.rollback()
            raise ex
        
        
        
        