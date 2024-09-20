from datetime import datetime
from typing import List, Union

from pydantic import BaseModel

from schemas.user import UserDisplay
from schemas.country import CountryDisplay


class QuestionBase(BaseModel):
    question: str


class QuestionEnhanced(BaseModel):
    original_question: str
    question: str | None
    valid: bool
    explanation: str | None

    class Config:
        from_attributes = True


class QuestionCreate(QuestionEnhanced):
    answer: bool | None
    user_id: int
    day_id: int
    context: str | None

    class Config:
        from_attributes = True


class QuestionDisplay(BaseModel):
    id: int
    original_question: str
    question: str | None
    valid: bool
    answer: bool | None
    user_id: int
    day_id: int
    asked_at: datetime

    class Config:
        from_attributes = True


class FullQuestionDisplay(QuestionDisplay):
    explanation: str

    class Config:
        from_attributes = True


class InvalidQuestionDisplay(BaseModel):
    id: int
    original_question: str
    valid: bool
    answer: bool | None
    user_id: int
    day_id: int
    asked_at: datetime

    explanation: str

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
    response: str
    guessed_at: datetime

    class Config:
        from_attributes = True


class UserHistory(BaseModel):
    user: UserDisplay
    questions: List[Union[QuestionDisplay, InvalidQuestionDisplay]]
    guesses: List[GuessDisplay]

    class Config:
        from_attributes = True


class FullUserHistory(BaseModel):
    user: UserDisplay
    questions: List[FullQuestionDisplay]
    guesses: List[GuessDisplay]

    class Config:
        from_attributes = True


class CountrydleState(BaseModel):
    user: UserDisplay
    questions_history: List[QuestionDisplay | InvalidQuestionDisplay]
    guess_history: List[GuessDisplay]
    remaining_questions: int
    remaining_guesses: int
    is_game_over: bool
    won: bool
    date: str


class CountrydleEndState(BaseModel):
    user: UserDisplay
    country: CountryDisplay
    questions_history: List[FullQuestionDisplay]
    guess_history: List[GuessDisplay]
    remaining_questions: int
    remaining_guesses: int
    is_game_over: bool
    won: bool
    date: str
