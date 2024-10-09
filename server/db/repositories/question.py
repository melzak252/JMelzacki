from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import DayCountry, Question, User
from schemas.countrydle import (
    QuestionCreate,
)


class QuestionsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, qid: int) -> Question | None:
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

    async def get_user_day_questions(
        self, user: User, day: DayCountry
    ) -> List[Question]:
        questions_result = await self.session.execute(
            select(Question)
            .where(Question.user_id == user.id, Question.day_id == day.id)
            .order_by(Question.id.asc())
        )
        return questions_result.scalars().all()
