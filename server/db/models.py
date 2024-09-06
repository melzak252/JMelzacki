from passlib.context import CryptContext
from pgvector.sqlalchemy import Vector
from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    verified = Column(Boolean, default=False, nullable=False)
    # Relationships
    questions = relationship("Question", back_populates="user")
    permissions = relationship(
        "Permission", secondary="user_permissions", viewonly=True
    )
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
    user_id = Column(Integer, ForeignKey("users.id"))
    permission_id = Column(Integer, ForeignKey("permissions.id"))


class Country(Base):
    __tablename__ = "countries"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    official_name = Column(String, nullable=False)
    wiki = Column(String, nullable=False)
    md_file = Column(String, nullable=False)
    document = relationship("Document", uselist=False, back_populates="country")


class DayCountry(Base):
    __tablename__ = "day_countries"

    id = Column(Integer, primary_key=True, index=True)
    country_id = Column(Integer, ForeignKey("countries.id"))
    date = Column(Date, nullable=False, default=func.now())

    country = relationship("Country")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    day_id = Column(Integer, ForeignKey("day_countries.id"))
    context = Column(String, nullable=False)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    explanation = Column(String, nullable=False)
    asked_at = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="questions")
    day = relationship("DayCountry")


class Guess(Base):
    __tablename__ = "guesses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    day_id = Column(Integer, ForeignKey("day_countries.id"))
    guess = Column(String, nullable=False)
    guessed_at = Column(DateTime, default=func.now())

    response = Column(String, nullable=False)

    user = relationship("User", back_populates="guesses")
    day = relationship("DayCountry")


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    country_id = Column(Integer, ForeignKey("countries.id"))
    content = Column(String, nullable=False)

    country = relationship("Country", back_populates="document")
    fragments = relationship("Fragment", back_populates="document")


class Fragment(Base):
    __tablename__ = "fragments"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    text = Column(String, nullable=False)
    embedding = Column(Vector(1536), nullable=False)

    document = relationship("Document", back_populates="fragments")


class SentEmail(Base):
    __tablename__ = "sent_emails"

    # Define the columns in the table
    id = Column(Integer, primary_key=True, index=True)
    recipient = Column(String(255), nullable=False)  # Email of the recipient
    subject = Column(String(255), nullable=False)  # Email subject
    body = Column(Text, nullable=False)  # Email body
    status = Column(String(50), nullable=False, default="sent")  # Status (e.g., sent, failed)
    created_at = Column(DateTime, default=func.now())  # Timestamp of when the email was sent

    def __repr__(self):
        return f"<SentEmail(id={self.id}, recipient='{self.recipient}', subject='{self.subject}')>"