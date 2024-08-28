from db import get_db
from db.models import User
from db.schemas.user import UserDisplay
from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .utils import get_current_user

load_dotenv()
router = APIRouter()


@router.get("/me", response_model=UserDisplay)
async def read_users_me(
    user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    return user
