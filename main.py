import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from loguru import logger
from app import webhooks
from app.config import settings
from app.database.redis import redis_client


# Remove the default logger
logger.remove()

# Add a logger that outputs to a file
logger.add("async_app.log", level=settings.LOG_LEVEL, rotation="50 MB", retention="10 days")

# Add a logger that outputs to stdout (Docker logs)
logger.add(sys.stdout, level=settings.LOG_LEVEL)

logger.info(f"Application name: {settings.PROJECT_NAME} and log level: {settings.LOG_LEVEL}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_client.init()
    logger.info("Starting up the application")
    yield
    await redis_client.close()
    logger.info("Shutting down the application")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    lifespan=lifespan
)

app.include_router(webhooks.router)

@app.get("/healthcheck", tags=["Root"])
async def health():
    """Check the API is running"""
    return {"status": "👌"}
