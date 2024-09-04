import datetime
from pydantic import BaseModel, EmailStr


class EmailCreate(BaseModel):
    recipient: EmailStr  # Ensures valid email address
    subject: str
    body: str

    class Config:
        from_attributes = True
        
class EmailModel(EmailCreate):
    id: int
    status: str  # E.g., 'sent', 'failed'
    created_at: datetime.datetime