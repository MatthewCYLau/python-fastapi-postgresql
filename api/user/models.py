from sqlalchemy import TIMESTAMP, Column, String, text
from typing import List
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from api.config.database import Base
import uuid

from api.order.models import Order


class User(Base):
    """User model."""

    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    email = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    hashed_password = Column(String, nullable=False)
    orders: Mapped[List["Order"]] = relationship()
