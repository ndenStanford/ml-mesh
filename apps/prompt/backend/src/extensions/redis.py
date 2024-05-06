"""Redis extension."""

# Standard Library
import json
from typing import Any, Dict

# 3rd party libraries
import xxhash
from redis import from_url
from redis_cache import RedisCache

# Source
from src.settings import get_settings


settings = get_settings()


class RedisDb(RedisCache):
    """Redisdb wrapper class."""

    def __init__(self, redis_client):
        super(RedisDb, self).__init__(
            redis_client=redis_client, key_serializer=self._generate_hash
        )

    @staticmethod
    def _generate_hash(key: Dict[str, Any]) -> str:
        """Generates a hash for a given key."""
        json_key = json.dumps(key, sort_keys=True)
        # Using xxhash for fast non-cryptographic hashing
        hashed_key = xxhash.xxh64_hexdigest(json_key)
        return hashed_key


redis = RedisDb(from_url(settings.REDIS_CONNECTION_STRING))
