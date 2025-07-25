from api.config.logging import get_logger
from api.order.models import Order
from api.order.repository import OrderRepository
from api.order.schemas import OrderBase

logger = get_logger(__name__)


class OrderService:
    def __init__(self, session):
        self.session = session
        self.repository = OrderRepository(session)

    def create_order(self, order_data: OrderBase) -> Order:
        return self.repository.create(order_data)
