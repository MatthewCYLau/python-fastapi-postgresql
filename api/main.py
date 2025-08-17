import time
from dotenv import load_dotenv
import os

from api.metrics.metrics import (
    REQUEST_COUNT,
    REQUEST_IN_PROGRESS,
    REQUEST_LATENCY,
    update_system_metrics,
)


load_dotenv(".env")

from fastapi import FastAPI, Request, Response
from api.config.logging import setup_logging, get_logger
from api.user.views import router as user_router
from api.product.views import router as product_router
from api.order.views import router as order_router
from api.auth.views import router as auth_router
from api.comment.views import router as comment_router
from api.config.database import Base, engine
from prometheus_client import (
    generate_latest,
    CONTENT_TYPE_LATEST,
    REGISTRY,
)


setup_logging()
logger = get_logger(__name__)

app = FastAPI()

if os.environ.get("DB_HOST"):
    Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(product_router)
app.include_router(order_router)
app.include_router(auth_router)
app.include_router(comment_router)


@app.get("/")
async def up():
    logger.info("Root endpoint called")
    return "Up!!"


@app.get("/ping")
async def pong():
    return "pong!"


@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    method = request.method
    path = request.url.path
    REQUEST_IN_PROGRESS.labels(method=method, path=path).inc()
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    status = response.status_code
    REQUEST_COUNT.labels(method=method, status=status, path=path).inc()
    REQUEST_LATENCY.labels(method=method, status=status, path=path).observe(duration)
    REQUEST_IN_PROGRESS.labels(method=method, path=path).dec()

    return response


@app.get("/metrics")
async def metrics():
    update_system_metrics()
    return Response(generate_latest(REGISTRY), media_type=CONTENT_TYPE_LATEST)
