from datetime import date
import random
from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Country, DayCountry, Guess, Question, User
from db.schemas.countrydle import GuessCreate, QuestionCreate, UserHistory
from db.repositories.country import CountryRepository


class CountrydleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    ### DayCountry
    async def get_day_county(self, dcid: int) -> DayCountry | None:
        result = await self.session.execute(
            select(DayCountry).where(DayCountry.id == dcid)
        )

        return result.scalars().first()

    async def get_today_country(self) -> DayCountry | None:
        result = await self.session.execute(
            select(DayCountry)
            .where(DayCountry.date == date.today())
            .order_by(DayCountry.id.desc())
        )

        return result.scalars().first()

    async def create_day_country(self, country: Country) -> DayCountry:
        new_entry = DayCountry(country_id=country.id)

        self.session.add(new_entry)

        try:
            await self.session.commit()  # Commit the transaction
            await self.session.refresh(new_entry)  # Refresh the instance to get the ID
        except Exception as ex:
            await self.session.rollback()
            raise ex

        return new_entry

    async def generate_new_day_country(self) -> DayCountry:
        countries = await CountryRepository(self.session).get_all_countries()
        if not countries:
            raise ValueError("No countries in database!")

        country = random.choice(countries)

        new_country = await self.create_day_country(country)

        return new_country

    ### Guess
    async def get_guess(self, gid: int) -> Guess | None:
        result = await self.session.execute(select(Guess).where(Guess.id == gid))

        return result.scalars().first()

    async def create_guess(self, guess: GuessCreate) -> Guess:
        new_entry = Guess(guess.model_dump())

        self.session.add(new_entry)

        try:
            await self.session.commit()  # Commit the transaction
            await self.session.refresh(new_entry)  # Refresh the instance to get the ID
        except Exception as ex:
            await self.session.rollback()
            raise ex

        return new_entry

    async def get_guesses_for_user_day(
        self, user: User, day: DayCountry
    ) -> List[Guess]:
        questions_result = await self.session.execute(
            select(Guess).where(Guess.user_id == user.id, Guess.day_id == day.id)
        )

        return questions_result.scalars().all()

    ### Question
    async def get_question(self, qid: int) -> Question | None:
        result = await self.session.execute(select(Question).where(Question.id == qid))

        return result.scalars().first()

    async def create_question(self, quesiton: QuestionCreate) -> Question:
        new_entry = Question(quesiton.model_dump())

        self.session.add(new_entry)

        try:
            await self.session.commit()  # Commit the transaction
            await self.session.refresh(new_entry)  # Refresh the instance to get the ID
        except Exception as ex:
            await self.session.rollback()
            raise ex

        return new_entry

    async def get_questions_for_user_day(
        self, user: User, day: DayCountry
    ) -> List[Question]:
        questions_result = await self.session.execute(
            select(Question).where(
                Question.user_id == user.id, Question.day_id == day.id
            )
        )
        return questions_result.scalars().all()

    ### History
    async def get_player_histiory_for_today(
        self, user: User, day: DayCountry
    ) -> UserHistory:
        questions = await self.get_questions_for_user_day(user, day)
        guesses = self.get_guesses_for_user_day(user, day)

        return UserHistory(user=user, questions=questions, guesses=guesses)
