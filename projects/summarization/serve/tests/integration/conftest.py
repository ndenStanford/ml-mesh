"""Conftest."""

# 3rd party libraries
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Source
from src.serve.model import SummarizationServedModel
from src.serve.server import get_model_server
from src.settings import get_settings


@pytest.fixture(scope="function")
def settings():
    """Settings fixture."""
    return get_settings()


@pytest.fixture(scope="function")
def summarization_model(settings) -> FastAPI:
    """App fixture."""
    # Source
    return SummarizationServedModel(name=settings.model_name)


@pytest.fixture
def test_client():
    """Test client fixture."""
    model_server = get_model_server()

    return TestClient(model_server)
