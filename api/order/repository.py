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
