from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime

from users.schemas import UserDisplay

class CountryBase(BaseModel):
    name: str
    official_name: str
    wiki: str
    md_file: str
    
    class Config:
        from_attributes = True
        
class CountryDisplay(CountryBase):
    id: int
    
    class Config:
        from_attributes = True

# Country Schema
class DayBase(BaseModel):
    country_id: int

class DayDisplay(DayBase):
    id: int
    date: date
    
    class Config:
        from_attributes = True

class DayCreate(DayBase):
    class Config:
        from_attributes = True

# Question Schema
class QuestionBase(BaseModel):
    question: str

class QuestionCreate(QuestionBase):
    user_id: int
    country_id: int
    answer: str

class QuestionDisplay(QuestionBase):
    id: int
    asked_at: datetime
    answer: str

    class Config:
        from_attributes = True

# Guess Schema
class GuessBase(BaseModel):
    guess: str

class GuessCreate(GuessBase):
    country_id: int

class GuessDisplay(GuessBase):
    id: int
    guessed_at: datetime
    response: str
    
    class Config:
        from_attributes = True


class UserHistory(BaseModel):
    user: UserDisplay
    questions: List[QuestionDisplay]
    guesses: List[GuessDisplay]