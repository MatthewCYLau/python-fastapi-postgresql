from datetime import datetime
from sqlalchemy import TIMESTAMP, Column, Numeric, String
from sqlalchemy.dialects.postgresql import UUID

from api.config.database import Base
import uuid


class Transaction(Base):
    """Transaction model."""

    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, index=True, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), default=datetime.now(), primary_key=True
    )
    amount = Column(Numeric, nullable=False)
    __table_args__ = (
        {
            "postgresql_partition_by": "RANGE (created_at)",
        },
    )
