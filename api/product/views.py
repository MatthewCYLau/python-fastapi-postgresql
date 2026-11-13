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
from api.utils.file_util import generate_filename_suffix

logger = get_logger(__name__)


router = APIRouter(prefix="/api/v1/products", tags=["products"])

query = "SELECT * FROM products;"
POPULAR_PRODUCTS = ["Product one"]


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


@router.get("/dataframe")
def get_products_dataframe():
    engine = get_database_engine()
    with engine.connect() as conn:
        result = pd.read_sql(query, conn.connection, chunksize=1)
        for df in result:
            if df.empty:
                continue
            first_row = df.iloc[0]
            product_name = first_row["name"]
            product_price = first_row["price"]
            logger.info(f"Product {product_name} has price {product_price}")

            popular_products_df = df[df["name"].isin(POPULAR_PRODUCTS)]

            if not popular_products_df.empty:
                logger.info(f"Popular product {product_name} found!")

    return "Done"


@router.post("/gcs-parquet")
def generate_products_gcs_parquet():
    engine = get_database_engine()
    bucket_name = CLOUD_STORAGE_BUCKET_NAME
    filename_suffix = generate_filename_suffix()

    destination_blob_name = f"processed_data/products_{filename_suffix}.parquet"

    with engine.connect() as conn:
        df = pd.read_sql(query, conn.connection)
        gcs_path = f"gs://{bucket_name}/{destination_blob_name}"

        df.to_parquet(gcs_path, engine="pyarrow", index=False)
        logger.info(f"Successfully uploaded Parquet artifact to {gcs_path}")

    return {
        "status": "success",
        "blob_name": destination_blob_name,
        "gcs_path": gcs_path,
    }


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

    except FileNotFoundError as e:
        logger.error(f"Parquet file not found in GCS: {gcs_path} - {e}")
        raise HTTPException(
            status_code=404, detail=f"Parquet file not found: {request.blob_name}"
        )
    except Exception as e:
        logger.error(f"Unexpected error reading Parquet from GCS: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while reading the Parquet file from cloud storage.",
        )
