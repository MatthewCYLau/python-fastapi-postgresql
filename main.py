from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
async def up():
    return "Up!"


@app.get("/ping")
async def pong():
    return "pong!"


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info")
