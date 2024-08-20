

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select, or_
from db.models import User
from sqlalchemy.ext.asyncio import AsyncSession

from users.schemas import UserCreate

async def get_user(username: str, session: AsyncSession) -> User:
    result = await session.execute(
        select(User).where(User.username == username)
    )
    user_in_db = result.scalars().first()
    
    return user_in_db

async def register_user(user: UserCreate, session: AsyncSession) -> User:
    result = await session.execute(
        select(User).where(or_(User.username == user.username, User.email == user.email))
    )
    user_in_db = result.scalars().first()


    if user_in_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = User.hash_password(user.password)
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    
    return new_user
            