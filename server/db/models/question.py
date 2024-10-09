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
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from db.base import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    day_id = Column(Integer, ForeignKey("day_countries.id"))
    context = Column(String)
    original_question = Column(String, nullable=False)
    question = Column(String)
    valid = Column(Boolean, nullable=False)
    answer = Column(Boolean)
    explanation = Column(String, nullable=False)
    asked_at = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="questions")
    day = relationship("DayCountry")
