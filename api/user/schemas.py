from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
import uuid


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    """User creation schema."""

    password: str
    dateOfBirth: str


class UserUpdate(BaseModel):
    password: str
    dateOfBirth: str


class UserResponse(UserBase):
    """User response schema."""

    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    created_at: datetime
    date_of_birth: datetime
    email_verified: bool


class Token(BaseModel):
    """Token schema."""

    access_token: str
    token_type: str = "bearer"


class LoginData(BaseModel):
    """Login data schema."""

    email: EmailStr
    password: str
