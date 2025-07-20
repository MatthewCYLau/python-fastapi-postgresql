from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
import uuid


class UserBase(BaseModel):
    email: EmailStr


class UserResponse(UserBase):
    """User response schema."""

    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    created_at: datetime
