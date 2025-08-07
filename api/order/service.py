from api.config.logging import get_logger
from api.order.models import Order
from api.order.repository import OrderRepository
from api.order.schemas import OrderBase, OrderResponse, OrdersCountResponse
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

    def get_orders_by_user_id(self, user_id) -> list[OrderResponse]:
        orders = self.repository.get_orders_by_user_id(user_id)
        return [OrderResponse.model_validate(order) for order in orders]

    def get_orders_count_by_product_id(self, product_id: str) -> OrdersCountResponse:
        count = self.repository.get_orders_count_by_product_id(product_id)
        return OrdersCountResponse.model_validate(
            {"count": count, "product_id": product_id}
        )
