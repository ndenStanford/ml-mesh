# type: ignore
"""Redis client."""

# 3rd party libraries
from redis import from_url
from redis.client import Redis


def get_client(url: str) -> Redis:
    """Gets the redis client.

    Args:
        url (str): Connection string

    Returns:
        redis.client.Redis: Redis client
    """
    try:
        client = from_url(url=url)
        client.ping()
    except ValueError as e:
        print(f"REDIS_CONNECTION_STRING is not valid: {e}.")
        raise
    except ConnectionError as e:
        print(f"Couldn't connect to Redis: {e}.")
        raise
    return client
