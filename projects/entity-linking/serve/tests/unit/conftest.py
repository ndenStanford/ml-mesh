"""Conftest."""

# Standard Library
from unittest.mock import MagicMock, patch

# 3rd party libraries
import pytest
from fastapi import FastAPI

# Internal libraries
from onclusiveml.serving.rest.serve import OnclusiveHTTPException

# Source
from src.serve.artifacts import ServedModelArtifacts
from src.serve.model import ServedBelaModel
from src.settings import get_settings


@pytest.fixture(scope="function")
def settings():
    """Settings fixture."""
    return get_settings()


@pytest.fixture(scope="function")
def model_server(settings, entity_linking_model) -> FastAPI:
    """Server fixture."""
    return ModelServer(configuration=settings, model=entity_linking_model)


@pytest.fixture(scope="function")
@patch("json.loads")
@patch("builtins.open")
def artifacts(mock_open, mock_json, settings):
    """Model artifacts fixture."""
    return ServedModelArtifacts(settings)


@pytest.fixture(scope="function")
def entity_linking_model(settings, artifacts):
    """App fixture."""
    model = ServedBelaModel(served_model_artifacts=artifacts)

    return model


@pytest.fixture(scope="function")
def served_model(entity_linking_model):
    """Served model fixture."""
    return entity_linking_model


@pytest.fixture
def mock_served_model(artifacts):
    """Served model prediciton fixture."""
    mock_model = ServedBelaModel(served_model_artifacts=artifacts)

    mock_model._predict = MagicMock(
        return_value=[
            {
                "entities": ["Q484876", "Q312"],
                "el_scores": [0.5, 0.6],
                "md_scores": [0.7, 0.8],
                "offsets": [0, 22],
                "lengths": [10, 5],
            }
        ]
    )
    return mock_model


@pytest.fixture
def mock_served_model_with_exception(artifacts):
    """Served model exceptions fixture."""
    mock_model = ServedBelaModel(served_model_artifacts=artifacts)

    def _mock_predict(*args, **kwargs):
        raise OnclusiveHTTPException(
            status_code=422,
            detail="The language reference 'invalid_language' could not be mapped, or the language could not be inferred from the content.",  # noqa
        )

    mock_model._predict = MagicMock(side_effect=_mock_predict)
    return mock_model


@pytest.fixture
def mock_served_model_with_second_exception(artifacts):
    """Model artifacts fixture."""
    mock_model = ServedBelaModel(served_model_artifacts=artifacts)

    def _mock_predict(*args, **kwargs):
        raise OnclusiveHTTPException(
            status_code=422,
            detail="The language reference '' could not be mapped, or the language could not be inferred from the content.",  # noqa
        )

    mock_model._predict = MagicMock(side_effect=_mock_predict)
    return mock_model
