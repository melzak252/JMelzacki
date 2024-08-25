# backend/db/models.py
from datetime import datetime, date
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Date
from .base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    # Relationships
    questions = relationship("Question", back_populates="user")
    permissions = relationship("Permission", secondary="user_permissions", viewonly=True)
    guesses = relationship("Guess", back_populates="user")
    
    @property
    def permission_names(self):
        return [permission.name for permission in self.permissions]
    
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def hash_password(password):
        return pwd_context.hash(password)
    
    
    
class Permission(Base):
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    
class UserPermission(Base):
    __tablename__ = "user_permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    permission_id = Column(Integer, ForeignKey('permissions.id'))
    
    
class Country(Base):
    __tablename__ = "countries"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    official_name = Column(String, nullable=False)
    wiki = Column(String, nullable=False)
    md_file = Column(String, nullable=False)
    

class DayCountry(Base):
    __tablename__ = "day_countries"

    id = Column(Integer, primary_key=True, index=True)
    country_id = Column(Integer, ForeignKey('countries.id'))
    date = Column(Date, nullable=False, default=func.now())
    
    country = relationship("Country")
    
    
class Question(Base):
    __tablename__ = 'questions'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    day_id = Column(Integer, ForeignKey('day_countries.id')) 
    context = Column(String, nullable=False)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    explanation = Column(String, nullable=False)
    asked_at = Column(DateTime, default=func.now())
    
    user = relationship("User", back_populates="questions")
    day = relationship("DayCountry")
    
class Guess(Base):
    __tablename__ = 'guesses'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    country_id = Column(Integer, ForeignKey('day_countries.id'))
    guess = Column(String, nullable=False)
    guessed_at = Column(DateTime, default=func.now())
    
    response = Column(String, nullable=False)
    
    user = relationship("User", back_populates="guesses")
    day = relationship("DayCountry")