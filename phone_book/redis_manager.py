import logging
import redis.asyncio as redis

from .settings import REDIS_HOST, REDIS_PORT


class RedisManager:
    redis_client: redis.Redis = None

    @classmethod
    async def connect(cls):
        try:
            cls.redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
        except redis.RedisError as e:
            logging.error(e)
            raise

    @classmethod
    async def close(cls):
        if cls.redis_client is not None:
            await cls.redis_client.aclose()

    @classmethod
    async def get(cls, key):
        return await cls.redis_client.get(key)

    @classmethod
    async def set(cls, key, value):
        return await cls.redis_client.set(key, value)

    @classmethod
    async def delete(cls, key):
        await cls.redis_client.delete(key)
