# Standard Library
from unittest.mock import patch

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.core.optimization import OnclusiveModelOptimizer
from onclusiveml.tracking import (
    TrackedModelCard,
    TrackedModelSpecs,
    TrackedModelTestFiles,
)


@pytest.fixture
def tracked_model_specs():
    return TrackedModelSpecs(
        project="project", model="model", api_token="api_token"
    )  # Provide appropriate parameters


@pytest.fixture
def tracked_model_card():
    tracked_model_test_files = TrackedModelTestFiles(
        inputs="inputs", inference_params="inference_params", predictions="predictions"
    )
    return TrackedModelCard(
        model_type="trained",
        model_artifact_attribute_path="model_artifact_attribute_path",
        model_test_files=tracked_model_test_files,
    )  # Provide appropriate parameters


@patch(
    "onclusiveml.core.optimization.OnclusiveModelOptimizer.create_tracked_model_version",
    return_value=None,
)
def test_onclusive_model_optimizer_initialize(
    mock_create_tracked_model_version, tracked_model_specs, tracked_model_card
):
    optimizer = OnclusiveModelOptimizer(tracked_model_specs, tracked_model_card)
    assert optimizer.tracked_model_specs == tracked_model_specs
    assert optimizer.model_card == tracked_model_card
    mock_create_tracked_model_version.assert_called_once()
