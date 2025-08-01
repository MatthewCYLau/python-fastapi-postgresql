from sqlalchemy import select
from api.config.exception import NotFoundException
from api.config.logging import get_logger
from api.order.models import Order

logger = get_logger(__name__)


class OrderRepository:
    """Repository for handling order database operations."""

    def __init__(self, session):
        self.session = session

    def create(self, order_data) -> Order:

        order = Order(user_id=order_data.user_id, product_id=order_data.product_id)
        self.session.add(order)
        self.session.commit()
        self.session.refresh(order)

        logger.info(f"Created order.")
        return order

    def get_by_id(self, order_id: str) -> Order | None:
        query = select(Order).where(Order.id == order_id).join(Order.product)
        result = self.session.execute(query)
        order = result.scalar_one_or_none()
        if not order:
            raise NotFoundException(f"Order with id {order_id} not found")
        return order

    def get_all(self) -> list[Order]:
        query = select(Order).join(Order.product)
        result = self.session.execute(query)
        return list(result.scalars().all())
