from pydantic import BaseModel, ConfigDict
from datetime import datetime
import uuid


class CommentBase(BaseModel):
    product_id: uuid.UUID
    body: str


class CommentResponse(CommentBase):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    created_at: datetime
