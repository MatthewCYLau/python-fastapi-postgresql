import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from api.config.database import get_session
from api.config.exception import BadRequestException
from api.config.logging import get_logger
from api.order.repository import OrderRepository
from api.order.schemas import OrderBase, OrderResponse
from api.order.service import OrderService
from api.utils.date_util import validate_date_string

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


@router.get("/", response_model=list[OrderResponse])
async def get_all_orders(
    session=Depends(get_session), startDate: str = None, endDate: str = None
) -> list[OrderResponse]:
    """Get all orders."""
    logger.debug("Fetching all orders")

    dates_input = [startDate, endDate]
    if all(dates_input) and not all([validate_date_string(i) for i in dates_input]):
        raise BadRequestException(
            detail="Invalid date input. Must be in format YYYY-MM-DD"
        )

    try:
        orders = OrderService(session).get_all_orders(startDate, endDate)
        logger.info(f"Retrieved {len(orders)} orders")
        return orders
    except Exception as e:
        logger.error(f"Failed to fetch orders: {str(e)}")
        raise


@router.get("/{order_id}", response_model=OrderResponse)
def get_order_by_id(
    order_id: uuid.UUID,
    session=Depends(get_session),
) -> OrderResponse:
    logger.info(f"Getting order {order_id}")
    try:
        order = OrderService(session).get_order_by_id(order_id)
        logger.info(f"Retrieved order {order_id}")
        return order
    except Exception as e:
        logger.error(f"Failed to fetch order {order_id}: {e}")
        raise


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(
    order_id: uuid.UUID,
    session=Depends(get_session),
):
    logger.info(f"Deleting order: {order_id}")
    OrderService(session).delete_order_by_id(order_id)
