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
    guesses = relationship("Guess", back_populates="user")
    
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def hash_password(password):
        return pwd_context.hash(password)

class DailyCountry(Base):
    __tablename__ = "daily_countries"

    id = Column(Integer, primary_key=True, index=True)
    country_name = Column(String, nullable=False)
    date = Column(Date, nullable=False, default=func.now())
    
    
class Question(Base):
    __tablename__ = 'questions'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    country_id = Column(Integer, ForeignKey('daily_countries.id'))
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    explanation = Column(String, nullable=False)
    asked_at = Column(DateTime, default=func.now())
    
    user = relationship("User", back_populates="questions")
    country = relationship("DailyCountry")
    
class Guess(Base):
    __tablename__ = 'guesses'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    country_id = Column(Integer, ForeignKey('daily_countries.id'))
    guess = Column(String, nullable=False)
    guessed_at = Column(DateTime, default=func.now())
    
    response = Column(String, nullable=False)
    
    user = relationship("User", back_populates="guesses")
    country = relationship("DailyCountry")