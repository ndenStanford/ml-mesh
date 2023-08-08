"""Conftest."""

# 3rd party libraries
import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def test_client(app):
    client = TestClient(app)
    yield client
