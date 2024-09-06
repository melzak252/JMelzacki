from typing import List

from pydantic import BaseModel, EmailStr


class PermissionBase(BaseModel):
    name: str

    class Config:
        from_attributes = True


class PermissionDisplay(PermissionBase):
    id: int

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class DevUser(BaseModel):
    id: int
    username: str
    email: EmailStr
    hashed_password: str

    class Config:
        from_attributes = True


class UserDisplay(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True

class GoogleSignIn(BaseModel):
    credential: str