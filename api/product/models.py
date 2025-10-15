from typing import List
from datetime import datetime
from sqlalchemy import TIMESTAMP, Column, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, relationship, mapped_column

from api.comment.models import Comment
from api.config.database import Base
import uuid


class Product(Base):
    """Product model."""

    __tablename__ = "products"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    name = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.now())
    comments: Mapped[List["Comment"]] = relationship()
    price = Column(Numeric, nullable=False)
