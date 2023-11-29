"""Conftest."""

# Standard Library
from unittest.mock import patch

# 3rd party libraries
import pytest

# Source
from src.serve.artifacts import ServedModelArtifacts
from src.serve.model import ServedIPTCModel
from src.settings import get_settings


@pytest.fixture(scope="function")
def settings():
    """Settings fixture."""
    return get_settings()


@pytest.fixture
def model_card():
    """Model card fixture."""
    return {
        "model_artifact_attribute_path": "model/some/other/dir",
        "model_test_files": {
            "inputs": "model/some/other/inputs",
            "inference_params": "model/some/other/inference_param",
            "predictions": "model/some/other/predictions",
        },
    }


@pytest.fixture(scope="function")
@patch("json.loads")
@patch("builtins.open")
def artifacts(mock_open, mock_json, settings):
    """Model artifacts fixture."""
    return ServedModelArtifacts(settings)


@pytest.fixture(scope="function")
def served_model(artifacts):
    """Served model fixture."""
    return ServedIPTCModel(served_model_artifacts=artifacts)
