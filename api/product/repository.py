from api.config.exception import AlreadyExistsException
from api.config.logging import get_logger
from api.product.models import Product

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
