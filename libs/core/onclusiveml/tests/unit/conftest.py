"""Conftest."""

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.tracking import (
    TrackedModelCard,
    TrackedModelSpecs,
    TrackedModelTestFiles,
)


@pytest.fixture
def tracked_model_specs() -> TrackedModelSpecs:
    """Generate TrackedModelSpecs for testing purposes.

    Returns:
        TrackedModelSpecs: An instance of TrackedModelSpecs initialized with dummy data.
    """
    return TrackedModelSpecs(
        project="project", model="model", api_token="api_token"
    )  # Provide appropriate parameters


@pytest.fixture
def tracked_model_card() -> TrackedModelCard:
    """Generate TrackedModelCard for testing purposes.

    Returns:
        TrackedModelCard: An instance of TrackedModelCard initialized with dummy data.
    """
    tracked_model_test_files = TrackedModelTestFiles(
        inputs="inputs", inference_params="inference_params", predictions="predictions"
    )
    return TrackedModelCard(
        model_type="trained",
        model_artifact_attribute_path="model_artifact_attribute_path",
        model_test_files=tracked_model_test_files,
    )  # Provide appropriate parameters
