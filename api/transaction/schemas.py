from pydantic import BaseModel, ConfigDict
from datetime import datetime
import uuid


class TransactionBase(BaseModel):
    amount: float
    name: str


class TransactionResponse(TransactionBase):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    created_at: datetime
