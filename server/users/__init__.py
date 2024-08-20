from fastapi import APIRouter
from .schemas import UserDisplay
from db import get_db
from db.models import User
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import UserDisplay
from .utils import verify_access_token, oauth2_scheme
import users.crud as ucrud


router = APIRouter()



@router.get("/me", response_model=UserDisplay)
async def read_users_me(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    username = verify_access_token(token)

    user: User = await ucrud.get_user(username, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user
    
