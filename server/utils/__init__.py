from datetime import date, timedelta
import logging


from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from db import AsyncSessionLocal
from db.base import Base
from db.models import *  # noqa: F403
from db.repositories.countrydle import CountrydleRepository
from sqlalchemy.ext.asyncio import AsyncEngine


async def generate_day_countries():
    async with AsyncSessionLocal() as session:
        c_repo = CountrydleRepository(session)
        last = await c_repo.get_last_added_day_country()
        delta: timedelta = (date.today() + timedelta(days=5)) - last.date
        for day_date in (last.date + timedelta(n) for n in range(delta.days)):
            print(f"Generating country for {day_date}")
            await c_repo.generate_new_day_country(day_date)


scheduler = AsyncIOScheduler()
scheduler.add_job(generate_day_countries, CronTrigger(hour=0, minute=1))
