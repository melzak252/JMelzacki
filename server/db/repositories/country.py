from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Country
from db.schemas.country import CountryBase


class CountryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, cid: int) -> Country:
        result = await self.session.execute(select(Country).where(Country.id == cid))

        return result.scalars().first()

    async def get_all_countries(self) -> List[Country]:
        result = await self.session.execute(select(Country))

        return list(result.scalars().all())

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
