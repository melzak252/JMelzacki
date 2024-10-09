from datetime import datetime
from typing import List, Union

from pydantic import BaseModel

from schemas.user import UserDisplay
from schemas.country import CountryCount, CountryDisplay, DayCountryDisplay


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
    answer: bool | None


class GuessDisplay(GuessBase):
    id: int
    answer: bool | None
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


class CountrydleStateSchema(BaseModel):
    questions: List[QuestionDisplay | InvalidQuestionDisplay] = []
    guesses: List[GuessDisplay] = []
    remaining_questions: int
    remaining_guesses: int
    questions_asked: int
    guesses_made: int
    is_game_over: bool
    won: bool

    class Config:
        from_attributes = True


class CountrydleEndStateSchema(BaseModel):
    questions: List[FullQuestionDisplay]
    guesses: List[GuessDisplay]
    remaining_questions: int
    remaining_guesses: int
    questions_asked: int
    guesses_made: int
    is_game_over: bool
    won: bool
    points: int

    class Config:
        from_attributes = True


class CountrydleStateResponse(BaseModel):
    user: UserDisplay
    date: str
    state: CountrydleStateSchema


class CountrydleEndStateResponse(BaseModel):
    user: UserDisplay
    country: CountryDisplay
    date: str
    state: CountrydleEndStateSchema


class CountrydleHistory(BaseModel):
    countries_count: List[CountryCount]
    daily_countries: List[DayCountryDisplay]

    class Config:
        from_attributes = True


class LeaderboardEntry(BaseModel):
    id: int
    username: str
    points: int
    streak: int
    wins: int
