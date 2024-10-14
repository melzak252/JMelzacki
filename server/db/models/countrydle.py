from passlib.context import CryptContext
from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    and_,
)
from sqlalchemy.orm import relationship, foreign
from sqlalchemy.sql import func

from db.base import Base
from db.models.guess import Guess
from db.models.question import Question
from db.models.user import User


class DayCountry(Base):
    __tablename__ = "day_countries"

    id = Column(Integer, primary_key=True, index=True)
    country_id = Column(Integer, ForeignKey("countries.id"))
    date = Column(Date, nullable=False, default=func.now())

    country = relationship("Country")


class CountrydleState(Base):
    __tablename__ = "countrydle_states"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    day_id = Column(Integer, ForeignKey("day_countries.id"))
    remaining_questions = Column(Integer, nullable=False, default=10)
    remaining_guesses = Column(Integer, nullable=False, default=3)
    questions_asked = Column(Integer, nullable=False, default=0)
    guesses_made = Column(Integer, nullable=False, default=0)
    is_game_over = Column(Boolean, nullable=False, default=False)
    won = Column(Boolean, nullable=False, default=False)
    points = Column(Integer, nullable=False, default=0)

    user = relationship("User")
    day = relationship("DayCountry")

    # Corrected relationship for questions with foreign() annotation
    questions = relationship(
        "Question",
        primaryjoin=and_(
            user_id
            == foreign(Question.user_id),  # Use foreign() to specify foreign key
            day_id == foreign(Question.day_id),  # Use foreign() to specify foreign key
        ),
        viewonly=True,
        lazy="select",
    )

    # Corrected relationship for guesses with foreign() annotation
    guesses = relationship(
        "Guess",
        primaryjoin=and_(
            user_id == foreign(Guess.user_id),  # Use foreign() to specify foreign key
            day_id == foreign(Guess.day_id),  # Use foreign() to specify foreign key
        ),
        viewonly=True,
        lazy="select",
    )
