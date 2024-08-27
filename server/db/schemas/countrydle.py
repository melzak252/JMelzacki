from datetime import datetime
from typing import List

from pydantic import BaseModel

from db.schemas.user import UserDisplay


class QuestionBase(BaseModel):
    question: str


class QuestionCreate(QuestionBase):
    answer: str
    user_id: int
    day_id: int
    explanation: str
    context: str

    class Config:
        from_attributes = True


class QuestionDisplay(QuestionCreate):
    id: int
    asked_at: datetime

    class Config:
        from_attributes = True


# Guess Schema
class GuessBase(BaseModel):
    guess: str


class GuessCreate(GuessBase):
    day_id: int
    user_id: int
    response: str


class GuessDisplay(GuessBase):
    id: int
    guessed_at: datetime

    class Config:
        from_attributes = True


class UserHistory(BaseModel):
    user: UserDisplay
    questions: List[QuestionDisplay]
    guesses: List[GuessDisplay]

    class Config:
        from_attributes = True
