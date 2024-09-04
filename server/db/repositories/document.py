from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Country, Document, Fragment
from schemas.country import CountryBase


class DocumentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, did: int) -> Document | None:
        result = await self.session.execute(select(Document).where(Document.id == did))

        return result.scalars().first()

    async def get_doc_for_country(self, country_id: int) -> Document | None:
        result = await self.session.execute(
            select(Document).where(Document.country_id == country_id)
        )

        return result.scalars().first()

    async def get_country_by_name(self, name: str) -> Country | None:
        result = await self.session.execute(
            select(Country).where(Country.name.ilike(name))
        )

        return result.scalars().first()

    async def create_country(self, country: CountryBase) -> Country:
        new_entry = Country(**country.model_dump())

        self.session.add(new_entry)

        try:
            await self.session.commit()  # Commit the transaction
            await self.session.refresh(new_entry)  # Refresh the instance to get the ID
        except Exception as ex:
            await self.session.rollback()
            raise ex

        return new_entry


class FragmentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, fid: int) -> Fragment | None:
        result = await self.session.execute(select(Fragment).where(Fragment.id == fid))

        return result.scalars().first()

    async def get_fragments_for_doc(self, doc_id: int) -> List[Fragment]:
        result = await self.session.execute(
            select(Fragment).where(Fragment.document_id == doc_id)
        )

        return result.scalars().all()
