from sqlalchemy import and_, delete, select, func
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

    def get_all(self, startDate, endDate) -> list[Order]:

        if startDate and endDate:
            query = (
                select(Order)
                .filter(
                    and_(Order.created_at <= endDate, Order.created_at >= startDate)
                )
                .join(Order.product)
            )
        else:
            query = select(Order).join(Order.product)
        result = self.session.execute(query)
        return list(result.scalars().all())

    def delete_order_by_id(self, order_id: str) -> None:

        query = delete(Order).where(Order.id == order_id)
        result = self.session.execute(query)

        if result.rowcount == 0:
            raise NotFoundException(f"Order with id {order_id} not found")

        self.session.commit()
        logger.info(f"Deleted order with id {order_id}")

    def get_orders_by_user_id(self, user_id) -> list[Order]:
        query = select(Order).where(Order.user_id == user_id).join(Order.product)
        result = self.session.execute(query)
        return list(result.scalars().all())

    def get_orders_count_by_product_id(self, product_id: str) -> int:
        statement = (
            select(func.count())
            .select_from(Order)
            .where(Order.product_id == product_id)
        )
        count: int = self.session.execute(statement).scalar()

        if not count:
            raise NotFoundException(f"Order with product id {product_id} not found")
        return count
