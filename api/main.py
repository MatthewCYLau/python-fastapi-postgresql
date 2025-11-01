from datetime import datetime, timezone
from dotenv import load_dotenv
import os

from api.metrics.metrics import (
    update_system_metrics,
)
from api.middleware.middlewares import MetricsMiddleware, RequestHeaderMiddleware


load_dotenv(".env")

from fastapi import FastAPI, Response
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler
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


def log_utc_time_now():
    logger.info(
        f"{'UTC time now:':<20}{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}"
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = BackgroundScheduler()
    scheduler.add_job(log_utc_time_now, "interval", minutes=1)
    scheduler.start()
    yield


app = FastAPI(lifespan=lifespan)

if os.environ.get("DB_HOST") or os.getenv("SQLITE_IN_MEMORY_DB"):
    Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(product_router)
app.include_router(order_router)
app.include_router(auth_router)
app.include_router(comment_router)
app.add_middleware(MetricsMiddleware)
app.add_middleware(RequestHeaderMiddleware)


@app.get("/")
async def up():
    logger.info("Root endpoint called")
    return "Up!!"


@app.get("/ping")
async def pong():
    return "pong!"


@app.get("/metrics")
async def metrics():
    update_system_metrics()
    return Response(generate_latest(REGISTRY), media_type=CONTENT_TYPE_LATEST)
