from sqlalchemy import TIMESTAMP, Column, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, relationship, mapped_column

from api.config.database import Base
import uuid


class Product(Base):
    """Product model."""

    __tablename__ = "products"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    name = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
