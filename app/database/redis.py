import aioredis
from loguru import logger
from ..config import settings

class RedisClient:
    def __init__(self):
        self.redis = None

    async def init(self):
        if self.redis is None:
            self.redis = await aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}")
            logger.info(f"Redis connected on host: {settings.REDIS_HOST}")

    async def close(self):
        if self.redis:
            await self.redis.close()
            self.redis = None
            logger.info("Redis connection closed")

    async def get(self, key):
        return await self.redis.get(key)

    async def set(self, key, value):
        await self.redis.set(key, value)

# Instance RedisClient
redis_client = RedisClient()
