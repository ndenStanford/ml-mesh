"""Redis test."""

# 3rd party libraries
import pytest
from redis_cache import RedisCache

# Source
from src.extensions.redis import redis


def test_get_cache():
    """Test get cache."""
    assert isinstance(redis, RedisCache)


@pytest.mark.parametrize(
    "prompt, hash",
    [
        ("Help me practice my Spanish vocab.", "474db2d6c5869055"),
        ("You are: AutoGPT designed to automate user's work.", "c29821a26c239267"),
    ],
)
def test_hashing(prompt, hash):
    """Test hashing."""
    assert hash == redis._generate_hash(prompt)
