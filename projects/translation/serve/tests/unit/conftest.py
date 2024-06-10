"""Conftest."""

# Standard Library
from unittest.mock import MagicMock

# 3rd party libraries
import pytest
from fastapi import FastAPI

# Internal libraries
from onclusiveml.serving.rest.serve import OnclusiveHTTPException

# Source
from src.serve.model import TranslationModel
from src.settings import get_settings


settings = get_settings()


@pytest.fixture(scope="function")
def settings():
    """Settings fixture."""
    return get_settings()


@pytest.fixture(scope="function")
def translation_model(settings) -> FastAPI:
    """App fixture."""
    # Source
    return TranslationModel()


@pytest.fixture(scope="function")
def model_server(settings, translation_model) -> FastAPI:
    """Server fixture."""
    return ModelServer(configuration=settings, model=translation_model)


@pytest.fixture
def mock_served_model_with_exception(settings):
    """Served model exceptions fixture."""
    mock_model = TranslationModel()

    def _mock_predict(*args, **kwargs):
        raise OnclusiveHTTPException(
            status_code=204,
            detail="The language reference 'invalid_language' could not be mapped, or the language could not be inferred from the content.",  # noqa
        )

    mock_model._predict = MagicMock(side_effect=_mock_predict)
    return mock_model
