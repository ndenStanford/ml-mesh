"""Conftest."""

# 3rd party libraries
import pytest
from fastapi.testclient import TestClient

# Source
from src.serve.server import get_model_server
from src.settings import get_settings


@pytest.fixture(scope="function")
def settings():
    """Settings fixture."""
    return get_settings()


@pytest.fixture(scope="function")
def test_client(settings):
    """Test client fixture."""
    model_server = get_model_server(settings)

    return TestClient(model_server)
