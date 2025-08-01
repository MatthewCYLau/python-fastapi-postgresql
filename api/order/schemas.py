from pydantic import BaseModel, ConfigDict
from datetime import datetime
import uuid
from api.product.schemas import ProductResponse


class OrderBase(BaseModel):
    user_id: uuid.UUID
    product_id: uuid.UUID


class OrderResponse(OrderBase):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    created_at: datetime
    product: ProductResponse
