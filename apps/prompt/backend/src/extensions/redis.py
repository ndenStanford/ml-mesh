"""Redis extension."""

# Standard Library
import json
from typing import Any, Dict

# 3rd party libraries
import redis
import xxhash
from redis_cache import RedisCache

# Source
from src.settings import get_settings


settings = get_settings()


class RedisDb:
    """Redisdb wrapper class."""

    def get_cache(self):
        """Returns redis client."""
        redis_client = redis.from_url(settings.REDIS_CONNECTION_STRING)
        cache = RedisCache(redis_client=redis_client, key_serializer=self.generate_hash)
        return cache

    @staticmethod
    def generate_hash(key: Dict[str, Any]) -> str:
        """Generates a hash for a given key."""
        json_key = json.dumps(key, sort_keys=True)
        # Using xxhash for fast non-cryptographic hashing
        hashed_key = xxhash.xxh64_hexdigest(json_key)
        return hashed_key


cache = RedisDb().get_cache()
