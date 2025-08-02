from api.config.logging import get_logger
from api.order.models import Order
from api.order.repository import OrderRepository
from api.order.schemas import OrderBase, OrderResponse
from api.product.repository import ProductRepository
from api.product.service import ProductService
from api.user.service import UserService

logger = get_logger(__name__)


class OrderService:
    def __init__(self, session):
        self.session = session
        self.repository = OrderRepository(session)

    def create_order(self, order_data: OrderBase) -> Order:

        user = UserService(self.session).get_user_by_id(order_data.user_id)

        product_repository = ProductRepository(self.session)
        product_service = ProductService(product_repository)

        product = product_service.get_product_by_id(order_data.product_id)

        if user and product:
            return self.repository.create(order_data)

    def get_all_orders(self, startDate, endDate) -> list[OrderResponse]:
        orders = self.repository.get_all(startDate, endDate)
        return [OrderResponse.model_validate(order) for order in orders]

    def get_order_by_id(self, order_id: int) -> OrderResponse:
        order = self.repository.get_by_id(order_id)
        return OrderResponse.model_validate(order)

    def delete_order_by_id(self, order_id: str) -> None:
        self.repository.delete_order_by_id(order_id)
