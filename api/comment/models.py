from sqlalchemy import TIMESTAMP, Column, ForeignKey, String
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from api.config.database import Base
import uuid


class Comment(Base):
    """Comment model."""

    __tablename__ = "comments"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    body = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.now())
    product_id: Mapped[UUID] = mapped_column(ForeignKey("products.id"))
