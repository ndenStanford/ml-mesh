"""Conftest."""

# 3rd party libs
import pytest
from fastapi.testclient import TestClient

# Source
from src.app import create_app


@pytest.fixture(scope="session")
def app():
    return create_app()


@pytest.fixture
def test_client(app):
    client = TestClient(app)
    yield client
