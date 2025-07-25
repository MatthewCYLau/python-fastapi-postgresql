from pydantic import BaseModel, ConfigDict
from datetime import datetime
import uuid


class OrderBase(BaseModel):
    user_id: str
    product_id: str


class OrderResponse(OrderBase):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    created_at: datetime
