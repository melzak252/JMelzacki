from typing import List

from pydantic import BaseModel


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
    email: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class DevUser(BaseModel):
    id: int
    username: str
    email: str
    hashed_password: str

    class Config:
        from_attributes = True


class UserDisplay(BaseModel):
    id: int
    username: str
    email: str
    permissions: List[PermissionDisplay]

    class Config:
        from_attributes = True
