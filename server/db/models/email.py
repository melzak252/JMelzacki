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


class SentEmail(Base):
    __tablename__ = "sent_emails"

    # Define the columns in the table
    id = Column(Integer, primary_key=True, index=True)
    recipient = Column(String(255), nullable=False)  # Email of the recipient
    subject = Column(String(255), nullable=False)  # Email subject
    body = Column(Text, nullable=False)  # Email body
    status = Column(
        String(50), nullable=False, default="sent"
    )  # Status (e.g., sent, failed)
    created_at = Column(
        DateTime, default=func.now()
    )  # Timestamp of when the email was sent

    def __repr__(self):
        return f"<SentEmail(id={self.id}, recipient='{self.recipient}', subject='{self.subject}')>"
