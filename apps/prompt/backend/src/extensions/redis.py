# 3rd party libraries
import redis
from redis_cache import RedisCache

# Source
from src.settings import get_settings


settings = get_settings()


class RedisDb:
    def get_cache(self):
        redis_client = redis.from_url(settings.REDIS_CONNECTION_STRING)
        cache = RedisCache(redis_client=redis_client)
        return cache


cache = RedisDb().get_cache()
