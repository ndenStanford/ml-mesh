"""Conftest."""

# 3rd party libraries
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Source
from src.serve.__main__ import model_server
from src.serve.artifacts import ServedModelArtifacts
from src.serve.model import ServedBelaModel
from src.settings import get_settings


@pytest.fixture(scope="function")
def settings():
    """Settings fixture."""
    return get_settings()


@pytest.fixture(scope="function")
def test_served_model_artifacts(settings):
    """Served model artifacts fixture."""
    return ServedModelArtifacts(settings=settings)


@pytest.fixture(scope="function")
def entity_linking_model(test_served_model_artifacts) -> FastAPI:
    """Entity linking model fixture."""
    return ServedBelaModel(test_served_model_artifacts)


@pytest.fixture
def test_client():
    """Test client fixture."""
    return TestClient(model_server)
