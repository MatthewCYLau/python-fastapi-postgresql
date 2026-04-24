from datetime import datetime

from sqlalchemy import and_, select
from api.config.logging import get_logger
from api.transaction.models import Transaction

logger = get_logger(__name__)


class TransactionRepository:
    """Repository for handling transaction database operations."""

    def __init__(self, session):
        self.session = session

    def create(self, transaction_data) -> Transaction:

        transaction = Transaction(
            name=transaction_data.name, amount=float(transaction_data.amount)
        )
        self.session.add(transaction)
        self.session.commit()
        self.session.refresh(transaction)

        logger.info(f"Created transaction: {transaction.name}")
        return transaction

    def get_all(self, startDate, endDate) -> list[Transaction]:

        if startDate and endDate:

            start_date_p = datetime.strptime(startDate, "%Y-%m-%d").date()
            end_date_p = datetime.strptime(endDate, "%Y-%m-%d").date()

            query = select(Transaction).filter(
                and_(
                    Transaction.created_at <= end_date_p,
                    Transaction.created_at >= start_date_p,
                )
            )
        else:
            query = select(Transaction)
        result = self.session.execute(query)
        return list(result.scalars().all())
