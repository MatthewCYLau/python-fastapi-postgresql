from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from api.config.database import get_session
from api.config.exception import BadRequestException
from api.config.logging import get_logger
from api.transaction.repository import TransactionRepository
from api.transaction.schemas import TransactionBase, TransactionResponse
from api.transaction.service import TransactionService
from api.utils.date_util import validate_date_string

logger = get_logger(__name__)


router = APIRouter(prefix="/api/v1/transactions", tags=["transactions"])


def get_transaction_service(
    session: Session = Depends(get_session),
) -> TransactionService:
    repository = TransactionRepository(session)
    return TransactionService(repository)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_transaction(
    transaction_data: TransactionBase,
    service: TransactionService = Depends(get_transaction_service),
):
    """Register a new transaction."""
    logger.info("Registering transaction")
    return service.create_transaction(transaction_data)


@router.get("/", response_model=list[TransactionResponse])
def get_all_transactions(
    service: TransactionService = Depends(get_transaction_service),
    startDate: str = None,
    endDate: str = None,
) -> list[TransactionResponse]:
    """Get all transactions."""
    dates_input = [startDate, endDate]
    if all(dates_input) and not all([validate_date_string(i) for i in dates_input]):
        raise BadRequestException(
            detail="Invalid date input. Must be in format YYYY-MM-DD"
        )
    try:
        transactions = service.get_all_transactions(startDate, endDate)
        logger.info(f"Retrieved {len(transactions)} transactions")
        return transactions
    except Exception as e:
        logger.error(f"Failed to fetch transactions: {str(e)}")
        raise
