from api.config.logging import get_logger
from api.transaction.models import Transaction
from api.transaction.repository import TransactionRepository
from api.transaction.schemas import TransactionBase, TransactionResponse

logger = get_logger(__name__)


class TransactionService:
    def __init__(self, repository: TransactionRepository):
        self.repository = repository

    def create_transaction(self, transaction_data: TransactionBase) -> Transaction:
        return self.repository.create(transaction_data)

    def get_all_transactions(self, startDate, endDate) -> list[TransactionResponse]:
        transactions = self.repository.get_all(startDate, endDate)
        return [
            TransactionResponse.model_validate(transaction)
            for transaction in transactions
        ]
