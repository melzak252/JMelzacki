from datetime import date, timedelta
import logging


from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from db import AsyncSessionLocal
from db.base import Base
from db.models import *  # noqa: F403
from db.repositories.countrydle import CountrydleRepository, CountrydleStateRepository
from sqlalchemy.ext.asyncio import AsyncEngine

from db.repositories.user import UserRepository


async def check_streaks():
    async with AsyncSessionLocal() as session:
        u_repo = UserRepository(session)
        cs_repo = CountrydleStateRepository(session)

        users = await u_repo.get_all_verified_users()
        yesterday = date.today() - timedelta(days=1)
        dc_yesterday = await CountrydleRepository(session).get_day_country_by_date(
            yesterday
        )

        if dc_yesterday is None:
            logging.error(f"DayCountry for {yesterday} not found.")
            return

        for user in users:
            points = await u_repo.get_user_points(user.id)
            if not points:
                points = await u_repo.add_user_points(user.id)

            yesterday_state = await cs_repo.get_player_countrydle_state(
                user, dc_yesterday
            )

            if yesterday_state is None or not yesterday_state.is_game_over:
                points.streak = 0

            await session.commit()


async def generate_day_countries():
    async with AsyncSessionLocal() as session:
        c_repo = CountrydleRepository(session)

        for day_date in (date.today() + timedelta(n) for n in range(5)):
            day_country = c_repo.get_day_country_by_date(day_date)
            if day_country is not None:
                logging.info(f"DayCountry for {day_date} already exists.")
                continue

            print(f"Generating country for {day_date}")
            await c_repo.generate_new_day_country(day_date)


scheduler = AsyncIOScheduler()
scheduler.add_job(generate_day_countries, CronTrigger(hour=0, minute=0))
scheduler.add_job(check_streaks, CronTrigger(hour=0, minute=0))
