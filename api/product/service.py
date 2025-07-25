from api.config.logging import get_logger
from api.product.models import Product
from api.product.repository import ProductRepository
from api.product.schemas import ProductBase

logger = get_logger(__name__)


class ProductService:
    def __init__(self, session):
        self.session = session
        self.repository = ProductRepository(session)

    def create_product(self, product_data: ProductBase) -> Product:
        return self.repository.create(product_data)
