"""Conftest."""

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.feature_store.settings import FeastFeatureStoreSettings
from onclusiveml.tracking import (
    TrackedModelCard,
    TrackedModelSettings,
    TrackedModelTestFiles,
    TrackingSettings,
)


class TopicModelParams(TrackingSettings):
    """Ground truth specification for model inference mode.

    Will be used as ground truth inputs for components downstream of `train` (e.g. `compile` and
    `serve`) during testing
    """

    # SentenceTransformer
    embedding_model: str = "embedding_model"


class TrackedTopicBaseModelCard(TrackedModelCard):
    """The model card for the base model of the keywords ML project."""

    model_params: TopicModelParams
    model_params: TopicModelParams


@pytest.fixture
def tracked_model_specs() -> TrackedModelSettings:
    """Generate TrackedModelSettings for testing purposes.

    Returns:
        TrackedModelSettings: An instance of TrackedModelSettings initialized with dummy data.
    """
    return TrackedModelSettings(
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

    return TrackedTopicBaseModelCard(
        model_type="trained",
        model_artifact_attribute_path="model_artifact_attribute_path",
        model_test_files=tracked_model_test_files,
        model_params=TopicModelParams(),
    )  # Provide appropriate parameters


@pytest.fixture
def feature_store_params() -> FeastFeatureStoreSettings:
    """Generate FeastFeatureStoreSettings for testing purposes.

    Returns:
        FeastFeatureStoreSettings: An instance of FeastFeatureStoreSettings initialized with dummy data.
    """
    return FeastFeatureStoreSettings()  # Provide appropriate parameters
