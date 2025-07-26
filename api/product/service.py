from api.config.logging import get_logger
from api.product.models import Product
from api.product.repository import ProductRepository
from api.product.schemas import ProductBase, ProductResponse

logger = get_logger(__name__)


class ProductService:
    def __init__(self, session):
        self.session = session
        self.repository = ProductRepository(session)

    def create_product(self, product_data: ProductBase) -> Product:
        return self.repository.create(product_data)

    def get_all_products(self) -> list[ProductResponse]:
        products = self.repository.get_all()
        return [ProductResponse.model_validate(product) for product in products]

    def get_product_by_id(self, product_id: int) -> ProductResponse:
        product = self.repository.get_by_id(product_id)
        return ProductResponse.model_validate(product)
