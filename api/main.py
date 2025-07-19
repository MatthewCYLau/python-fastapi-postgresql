from fastapi import FastAPI
import uvicorn
from api.config.logging import setup_logging, get_logger

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


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info")
