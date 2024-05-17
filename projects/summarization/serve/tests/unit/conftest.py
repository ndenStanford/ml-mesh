"""Conftest."""

# 3rd party libraries
import pytest
from fastapi import FastAPI

# Source
from src.serve.model import SummarizationServedModel
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
