from sqlalchemy import TIMESTAMP, Column, text, ForeignKey, Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, relationship, mapped_column

from api.config.database import Base
import uuid

from api.product.models import Product


class Order(Base):
    """Order model."""

    __tablename__ = "orders"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    product_id: Mapped[UUID] = mapped_column(ForeignKey("products.id"))
    product: Mapped["Product"] = relationship()
    quantity = Column(Integer, nullable=False)
    total_cost = Column(Numeric, nullable=False)
