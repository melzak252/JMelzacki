import logging


from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from db import AsyncSessionLocal
from db.base import Base
from db.models import *  # noqa: F403
from db.repositories.countrydle import CountrydleRepository
from sqlalchemy.ext.asyncio import AsyncEngine

async def generate_country_for_today():
    async with AsyncSessionLocal() as session:
        await CountrydleRepository(session).generate_new_day_country()
        
scheduler = AsyncIOScheduler()
scheduler.add_job(generate_country_for_today, CronTrigger(hour=0, minute=1))

