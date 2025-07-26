import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from api.config.database import get_session
from api.config.logging import get_logger
from api.product.repository import ProductRepository
from api.product.schemas import ProductBase, ProductResponse
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


@router.get("/", response_model=list[ProductResponse])
def get_all_products(
    session=Depends(get_session),
) -> list[ProductResponse]:
    """Get all products."""
    logger.debug("Fetching all products")
    try:
        products = ProductService(session).get_all_products()
        logger.info(f"Retrieved {len(products)} products")
        return products
    except Exception as e:
        logger.error(f"Failed to fetch products: {str(e)}")
        raise


@router.get("/{product_id}", response_model=ProductResponse)
def get_product_by_id(
    product_id: uuid.UUID,
    session=Depends(get_session),
) -> ProductResponse:
    logger.info(f"Getting product {product_id}")
    try:
        product = ProductService(session).get_product_by_id(product_id)
        logger.info(f"Retrieved product {product_id}")
        return product
    except Exception as e:
        logger.error(f"Failed to fetch product {product_id}: {e}")
        raise


@router.patch("/{product_id}", response_model=ProductResponse)
def update_product_by_id(
    product_id: uuid.UUID,
    product_data: ProductBase,
    session=Depends(get_session),
) -> ProductResponse:
    """Update product by ID."""
    logger.debug(f"Updating product {product_id}")
    try:
        product = ProductService(session).update_product_by_id(product_id, product_data)
        logger.info(f"Updated product {product_id}")
        return product
    except Exception as e:
        logger.error(f"Failed to update product {product_id}: {str(e)}")
        raise
