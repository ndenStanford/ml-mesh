"""Conftest."""

# 3rd party libraries
import pytest

# Source
from src.serve.artifacts import ServedModelArtifacts
from src.serve.model import ServedNERModel
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
def artifacts(settings):
    """Model artifacts fixture."""
    return ServedModelArtifacts(settings)


@pytest.fixture(scope="function")
def served_model(artifacts):
    """Served model fixture."""
    return ServedNERModel(served_model_artifacts=artifacts)
