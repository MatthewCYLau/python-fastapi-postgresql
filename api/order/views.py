from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from api.config.database import get_session
from api.config.logging import get_logger
from api.order.repository import OrderRepository
from api.order.schemas import OrderBase
from api.order.service import OrderService

logger = get_logger(__name__)


router = APIRouter(prefix="/api/v1/orders", tags=["orders"])


def get_order_service(session: Session = Depends(get_session)) -> OrderService:
    repository = OrderRepository(session)
    return OrderService(repository)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_order(order_data: OrderBase, session=Depends(get_session)):
    """Register a new order."""
    logger.info(
        f"Registering order for user ID {order_data.user_id} and product ID {order_data.product_id}"
    )
    return OrderService(session).create_order(order_data)
