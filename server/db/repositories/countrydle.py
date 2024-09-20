from datetime import date
import random
from typing import List, Tuple
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Country, DayCountry, Guess, Question, User
from schemas.countrydle import (
    CountrydleEndState,
    CountrydleState,
    FullUserHistory,
    GuessCreate,
    InvalidQuestionDisplay,
    QuestionCreate,
    QuestionDisplay,
    UserHistory,
)
from db.repositories.country import CountryRepository


class CountrydleRepository:
    MAX_GUESSES = 3
    MAX_QUESTIONS = 10

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
        new_entry = Guess(**guess.model_dump())

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
        new_entry = Question(**quesiton.model_dump())

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
            select(Question)
            .where(Question.user_id == user.id, Question.day_id == day.id)
            .order_by(Question.id.asc())
        )
        return questions_result.scalars().all()

    ### History
    async def get_player_histiory_for_today(
        self, user: User, day: DayCountry
    ) -> UserHistory:
        questions = [
            (
                QuestionDisplay.model_validate(question)
                if question.valid
                else InvalidQuestionDisplay.model_validate(question)
            )
            for question in await self.get_questions_for_user_day(user, day)
        ]

        guesses = await self.get_guesses_for_user_day(user, day)

        return UserHistory(user=user, questions=questions, guesses=guesses)

    async def get_player_full_histiory_for_today(
        self, user: User, day: DayCountry
    ) -> FullUserHistory:
        questions = await self.get_questions_for_user_day(user, day)
        guesses = await self.get_guesses_for_user_day(user, day)

        return FullUserHistory(user=user, questions=questions, guesses=guesses)

    async def is_player_game_over(self, player: User, day: DayCountry) -> bool:
        guesses: List[Guess] = await self.get_guesses_for_user_day(player, day)

        if len(guesses) >= 3:
            return True

        if any(g.response == "True" for g in guesses):
            return True

        return False

    async def get_game_result(self, user: User, day: DayCountry) -> Tuple[bool, bool]:
        guesses: List[Guess] = await self.get_guesses_for_user_day(user, day)
        won = any(g.response == "True" for g in guesses)
        game_over = len(guesses) >= 3 or won
        return game_over, won

    async def get_game_state(self, user: User, day: DayCountry) -> CountrydleState:
        questions = [
            (
                QuestionDisplay.model_validate(question)
                if question.valid
                else InvalidQuestionDisplay.model_validate(question)
            )
            for question in await self.get_questions_for_user_day(user, day)
        ]
        guesses = await self.get_guesses_for_user_day(user, day)
        question_asked = len(questions)
        guesses_made = len(guesses)
        game_over, won = await self.get_game_result(user, day)
        return CountrydleState(
            user=user,
            questions_history=questions,
            guess_history=guesses,
            remaining_questions=self.MAX_QUESTIONS - question_asked,
            remaining_guesses=self.MAX_GUESSES - guesses_made,
            is_game_over=game_over,
            won=won,
            date=str(day.date),
        )

    async def get_end_game_state(
        self, user: User, day: DayCountry
    ) -> CountrydleEndState:
        questions = await self.get_questions_for_user_day(user, day)
        guesses = await self.get_guesses_for_user_day(user, day)
        question_asked = len(questions)
        guesses_made = len(guesses)
        game_over, won = await self.get_game_result(user, day)
        country = await CountryRepository(self.session).get(day.country_id)
        return CountrydleEndState(
            user=user,
            country=country,
            questions_history=questions,
            guess_history=guesses,
            remaining_questions=self.MAX_QUESTIONS - question_asked,
            remaining_guesses=self.MAX_GUESSES - guesses_made,
            is_game_over=game_over,
            won=won,
            date=str(day.date),
        )
