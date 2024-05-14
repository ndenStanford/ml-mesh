"""Redis cache backend."""

# 3rd party libraries
import pytest

# Source
from src.extensions.redis import redis


@pytest.mark.order(4)
def test_set():
    """Test redis client set."""
    assert redis.client.get("integration") is None
    redis.client.set("integration", "value")
    assert redis.client.get("integration") == b"value"


@pytest.mark.order(5)
def test_delete():
    """Test redis client set."""
    redis.client.delete("integration")
    assert redis.client.get("integration") is None
