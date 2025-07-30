from sqlalchemy import delete, select, update
from api.config.exception import NotFoundException
from api.config.logging import get_logger
from api.product.models import Product
from api.product.schemas import ProductBase

logger = get_logger(__name__)


class ProductRepository:
    """Repository for handling product database operations."""

    def __init__(self, session):
        self.session = session

    def create(self, product_data) -> Product:

        product = Product(name=product_data.name)
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)

        logger.info(f"Created product: {product.name}")
        return product

    def get_by_id(self, product_id: str) -> Product | None:
        query = select(Product).where(Product.id == product_id)
        result = self.session.execute(query)
        product = result.scalar_one_or_none()
        if not product:
            raise NotFoundException(f"Product with id {product_id} not found")
        return product

    def get_all(self) -> list[Product]:
        query = select(Product)
        result = self.session.execute(query)
        return list(result.scalars().all())

    def update_by_id(self, product_id: str, product_data: ProductBase) -> Product:
        """Update product by ID.

        Args:
            product_id: Product ID
            product_data: Product update data

        Returns:
            Product: Updated product

        Raises:
            NotFoundException: If product not found
        """
        update_data = product_data.model_dump(exclude_unset=True)
        if not update_data:
            raise ValueError("No fields to update")

        query = update(Product).where(Product.id == product_id).values(**update_data)
        result = self.session.execute(query)

        if result.rowcount == 0:
            raise NotFoundException(f"Product with id {product_id} not found")

        self.session.commit()
        return self.get_by_id(product_id)

    def delete_product_by_id(self, product_id: str) -> None:

        query = delete(Product).where(Product.id == product_id)
        result = self.session.execute(query)

        if result.rowcount == 0:
            raise NotFoundException(f"Product with id {product_id} not found")

        self.session.commit()
        logger.info(f"Deleted product with id {product_id}")
