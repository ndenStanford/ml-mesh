"""Conftest."""

# 3rd party libraries
import pytest
from fastapi import FastAPI

# Source
from src.serve.model import EntityLinkingServedModel
from src.settings import get_settings


@pytest.fixture(scope="function")
def settings():
    """Settings fixture."""
    return get_settings()


@pytest.fixture(scope="function")
def entity_linking_model(settings) -> FastAPI:
    """App fixture."""
    # Source
    return EntityLinkingServedModel(name=settings.model_name)


@pytest.fixture(scope="function")
def model_server(settings, entity_linking_model) -> FastAPI:
    """Server fixture."""
    return ModelServer(configuration=settings, model=entity_linking_model)
