"""Conftest."""

# 3rd party libraries
import pytest


@pytest.fixture
def test_model_card():

    return {
        "model_artifact_attribute_path": "model/some/other/dir",
        "model_test_files": {
            "inputs": "model/some/other/inputs",
            "inference_params": "model/some/other/inference_param",
            "predictions": "model/some/other/predictions",
        },
    }
