from api.config.logging import get_logger
from api.order.models import Order
from api.order.repository import OrderRepository
from api.order.schemas import OrderBase, OrderResponse

logger = get_logger(__name__)


class OrderService:
    def __init__(self, session):
        self.session = session
        self.repository = OrderRepository(session)

    def create_order(self, order_data: OrderBase) -> Order:
        return self.repository.create(order_data)

    def get_all_orders(self) -> list[OrderResponse]:
        orders = self.repository.get_all()
        return [OrderResponse.model_validate(order) for order in orders]

    def get_order_by_id(self, order_id: int) -> OrderResponse:
        order = self.repository.get_by_id(order_id)
        return OrderResponse.model_validate(order)

    def delete_order_by_id(self, order_id: str) -> None:
        self.repository.delete_order_by_id(order_id)
