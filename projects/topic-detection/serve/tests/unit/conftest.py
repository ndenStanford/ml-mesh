"""Conftest."""

# 3rd party libraries
import pytest
from fastapi.testclient import TestClient

# Source
from src.app import create_app


@pytest.fixture(scope="session")
def app():
    """App fixture."""
    return create_app()


@pytest.fixture
def test_client(app):
    """Test client fixture."""
    client = TestClient(app)
    yield client
