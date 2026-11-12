import uuid
from fastapi import APIRouter, Depends, HTTPException, status
import pandas as pd
from sqlalchemy.orm import Session
from api.config.constants import CLOUD_STORAGE_BUCKET_NAME
from api.config.database import get_database_engine, get_session, get_read_only_session
from api.config.logging import get_logger
from api.product.repository import ProductRepository
from api.product.schemas import ParquetRequest, ProductBase, ProductResponse
from api.product.service import ProductService

logger = get_logger(__name__)


router = APIRouter(prefix="/api/v1/products", tags=["products"])


def get_product_service(session: Session = Depends(get_session)) -> ProductService:
    repository = ProductRepository(session)
    return ProductService(repository)


def get_read_only_product_service(
    session: Session = Depends(get_read_only_session),
) -> ProductService:
    repository = ProductRepository(session)
    return ProductService(repository)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: ProductBase, service: ProductService = Depends(get_product_service)
):
    """Register a new product."""
    logger.info(f"Registering product: {product_data.name}")
    return service.create_product(product_data)


@router.get("/", response_model=list[ProductResponse])
def get_all_products(
    service: ProductService = Depends(get_read_only_product_service),
    limit: int = None,
    pageSize: int = 5,
    currentPage: int = 1,
) -> list[ProductResponse]:
    """Get all products."""
    logger.debug("Fetching all products")
    try:
        products = service.get_all_products(limit, pageSize, currentPage)
        logger.info(f"Retrieved {len(products)} products")
        return products
    except Exception as e:
        logger.error(f"Failed to fetch products: {str(e)}")
        raise


@router.get("/{product_id}", response_model=ProductResponse)
def get_product_by_id(
    product_id: uuid.UUID,
    service: ProductService = Depends(get_product_service),
) -> ProductResponse:
    logger.info(f"Getting product {product_id}")
    try:
        product = service.get_product_by_id(product_id)
        logger.info(f"Retrieved product {product_id}")
        return product
    except Exception as e:
        logger.error(f"Failed to fetch product {product_id}: {e}")
        raise


@router.patch("/{product_id}", response_model=ProductResponse)
def update_product_by_id(
    product_id: uuid.UUID,
    product_data: ProductBase,
    service: ProductService = Depends(get_product_service),
) -> ProductResponse:
    """Update product by ID."""
    logger.debug(f"Updating product {product_id}")
    try:
        product = service.update_product_by_id(product_id, product_data)
        logger.info(f"Updated product {product_id}")
        return product
    except Exception as e:
        logger.error(f"Failed to update product {product_id}: {str(e)}")
        raise


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: uuid.UUID,
    service: ProductService = Depends(get_product_service),
):
    logger.info(f"Deleting product: {product_id}")
    service.delete_product_by_id(product_id)


@router.post("/gcs-parquet")
def generate_products_gcs_parquet():
    engine = get_database_engine()
    destination_blob_name = "processed_data/products.parquet"
    bucket_name = CLOUD_STORAGE_BUCKET_NAME

    with engine.connect() as conn:
        query = "SELECT * FROM products;"
        df = pd.read_sql(query, conn.connection)
        gcs_path = f"gs://{bucket_name}/{destination_blob_name}"
        df.to_parquet(gcs_path, engine="pyarrow", index=False)

        logger.info(f"Successfully uploaded Parquet artifact to {gcs_path}")

    return "Ok"


@router.post("/df-from-parquet")
def get_parquet_dataframe_from_parquet(request: ParquetRequest):
    bucket_name = CLOUD_STORAGE_BUCKET_NAME
    gcs_path = f"gs://{bucket_name}/{request.blob_name}"

    try:
        df = pd.read_parquet(gcs_path, engine="pyarrow")
        logger.info(f"Successfully read Parquet file from {gcs_path} ({len(df)} rows)")

        return {
            "status": "success",
            "blob_name": request.blob_name,
            "row_count": len(df),
            "data": df.to_dict(orient="records"),
        }

    except Exception as e:
        logger.error(f"Error reading Parquet from GCS: {e}")
        raise HTTPException(
            status_code=400, detail=f"Failed to read Parquet file: {str(e)}"
        )
