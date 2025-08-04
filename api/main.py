from dotenv import load_dotenv
import os

load_dotenv(".env")

from fastapi import FastAPI
from api.config.logging import setup_logging, get_logger
from api.user.views import router as user_router
from api.product.views import router as product_router
from api.order.views import router as order_router
from api.auth.views import router as auth_router
from api.comment.views import router as comment_router
from api.config.database import Base, engine


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
    return "Up!"


@app.get("/ping")
async def pong():
    return "pong!"
