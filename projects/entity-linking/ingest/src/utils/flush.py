# type: ignore
"""Flush database."""

# Source
from src.settings import get_settings
from src.utils.client import get_client


if __name__ == "__main__":
    settings = get_settings()
    client = get_client(url=settings.REDIS_CONNECTION_STRING)
    client.flushdb()
