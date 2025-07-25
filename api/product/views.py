import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from api.config.database import get_session
from api.config.logging import get_logger
from api.product.repository import ProductRepository
from api.product.schemas import ProductBase
from api.product.service import ProductService

logger = get_logger(__name__)


router = APIRouter(prefix="/api/v1/products", tags=["products"])


def get_product_service(session: Session = Depends(get_session)) -> ProductService:
    repository = ProductRepository(session)
    return ProductService(repository)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_product(product_data: ProductBase, session=Depends(get_session)):
    """Register a new product."""
    logger.info(f"Registering product: {product_data.name}")
    return ProductService(session).create_product(product_data)
