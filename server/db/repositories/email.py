from fastapi import HTTPException
from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import SentEmail
from schemas.email import EmailCreate


class EmailRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, emid) -> SentEmail | None:
        result = await self.session.execute(select(SentEmail).where(SentEmail.id == emid))

        return result.scalars().first()
    

    async def add_email(self, email: EmailCreate) -> SentEmail:
        new_sentemail = SentEmail(
            **email.model_dump()
        )
        self.session.add(new_sentemail)
        await self.session.commit()
        await self.session.refresh(new_sentemail)

        return new_sentemail