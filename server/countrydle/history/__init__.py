from db import get_db
from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.countrydle import CountrydleHistory
from db.repositories.countrydle import CountrydleRepository


load_dotenv()

router = APIRouter(prefix="/history")


@router.get("/all", response_model=CountrydleHistory)
async def gey_history(session: AsyncSession = Depends(get_db)):
    daily_countries = await CountrydleRepository(session).get_countrydle_history()
    countries_count = await CountrydleRepository(session).get_countries_count()
    return CountrydleHistory(
        daily_countries=daily_countries,
        countries_count=countries_count,
    )
