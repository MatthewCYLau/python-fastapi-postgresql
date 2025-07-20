from dotenv import load_dotenv
from fastapi import FastAPI
from api.config.logging import setup_logging, get_logger

load_dotenv(".env")

setup_logging()
logger = get_logger(__name__)

app = FastAPI()


@app.get("/")
async def up():
    logger.info("Root endpoint called")
    return "Up!"


@app.get("/ping")
async def pong():
    return "pong!"
