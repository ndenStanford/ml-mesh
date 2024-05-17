# type: ignore
"""Flush database."""

# 3rd party libraries
from redis import from_url

# Source
from src.settings import get_settings


if __name__ == "__main__":
    settings = get_settings()
    try:
        client = from_url(url=settings.REDIS_CONNECTION_STRING)
    except ValueError as e:
        print(f"REDIS_CONNECTION_STRING is not valid: {e}")
        raise
    client.flushdb()
