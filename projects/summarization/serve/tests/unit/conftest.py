"""Conftest."""

import pytest
from fastapi.testclient import TestClient

from src.app import create_app


@pytest.fixture(scope="session")
def app():
    return create_app()


@pytest.fixture
def client_test(app):
    client = TestClient(app)
    yield client
