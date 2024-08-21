from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timezone


class User(BaseModel):
    username: str
    password: str
    email: EmailStr
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
