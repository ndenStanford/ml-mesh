"""Conftest."""

# 3rd party libraries
import pytest
from fastapi.testclient import TestClient

# Source
from src._init import _setup_prompts
from src.app import create_app


@pytest.fixture(scope="session")
def app():
    # A bit of a hack to get the promt to initialize in the test pipeline
    _setup_prompts()
    return create_app()


@pytest.fixture
def test_client(app):
    client = TestClient(app)
    yield client
