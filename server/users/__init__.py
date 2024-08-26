from db import get_db
from db.models import User
from db.schemas.user import UserDisplay
from dotenv import load_dotenv
from fastapi import APIRouter, Cookie, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import users.crud as ucrud

from .utils import verify_access_token

load_dotenv()
router = APIRouter()

@router.get("/me", response_model=UserDisplay)
async def read_users_me(access_token: str = Cookie(None), db: AsyncSession = Depends(get_db)):
    username = verify_access_token(access_token)

    user: User = await ucrud.get_user(username, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user
    
