import re
from fastapi import HTTPException
from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Permission, User
from schemas.user import UserCreate


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    def verify_password(password, db_password):
        return User.verify_password(password, db_password)

    async def get(self, uid) -> User | None:
        result = await self.session.execute(select(User).where(User.id == uid))

        return result.scalars().first()

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(select(User).where(User.email == email))

        return result.scalars().first()
    
    async def get_veified_user(self, uid) -> User | None:
        result = await self.session.execute(select(User).where(and_(User.id == uid, User.verified == True)))

        return result.scalars().first()
    
    async def get_user(self, username: str) -> User | None:
        result = await self.session.execute(
            select(User).where(User.username == username)
        )
        return result.scalars().first()

    async def register_user(self, user: UserCreate) -> User:
        if re.fullmatch("^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$", user.username):
            raise HTTPException(status_code=400, detail="Username cannot be an email address!")
        
        if not re.fullmatch("^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$", user.email):
            raise HTTPException(status_code=400, detail="Email is not valid email address!")
        
        result = await self.session.execute(
            select(User).where(
                User.username == user.username
            )
        )
        user_in_db = result.scalars().first()

        if user_in_db:
            raise HTTPException(status_code=400, detail="Username already taken!")
        
        result = await self.session.execute(
            select(User).where(
                User.email == user.email
            )
        )
        user_in_db = result.scalars().first()

        if user_in_db:
            raise HTTPException(status_code=400, detail="Email already taken!")
        
        hashed_password = User.hash_password(user.password)
        new_user = User(
            username=user.username, email=user.email, hashed_password=hashed_password
        )
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)

        return new_user
    
    async def register_by_google(self, token_info: dict) -> User:
        user = await self.get_by_email(token_info["email"])
        if user:
            raise HTTPException(status_code=400, detail="Email already taken!")
        
        new_user = User(
            username=token_info["email"], email=token_info["email"], verified=True
        )
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)

        return new_user

    async def verify_user_email(self, email: str):
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        
        user = result.scalar_one()
        user.verified = True
        await self.session.commit()
        
        return user

class PermissionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, pid: int) -> Permission | None:
        res = await self.session.execute(select(Permission).where(Permission.id == pid))

        return res.scalars().all()

    async def get_by_name(self, name: str) -> Permission | None:
        res = await self.session.execute(
            select(Permission).where(Permission.name.ilike(name))
        )

        return res.scalars().all()

    async def create_permission(self, name: str) -> Permission:
        perm = await self.get_by_name(name)
        if perm:
            raise HTTPException(
                status_code=400, detail=f"There is already permission with name {name}"
            )

        new_user = Permission(name=name)
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)

        return new_user
