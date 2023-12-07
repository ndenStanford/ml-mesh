"""Conftest."""

# 3rd party libraries
import pytest

# Source
from src.settings import get_settings


@pytest.fixture(scope="function")
def settings():
    """Settings fixture."""
    return get_settings()
