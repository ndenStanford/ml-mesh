"""Conftest."""
# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.data.feature_store import FeatureStoreParams
from onclusiveml.tracking import (
    TrackedModelCard,
    TrackedModelSpecs,
    TrackedModelTestFiles,
    TrackedParams,
)


class TopicModelParams(TrackedParams):
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

    return TrackedTopicBaseModelCard(
        model_type="trained",
        model_artifact_attribute_path="model_artifact_attribute_path",
        model_test_files=tracked_model_test_files,
        model_params=TopicModelParams(),
    )  # Provide appropriate parameters


@pytest.fixture
def feature_store_params() -> FeatureStoreParams:
    """Generate FeatureStoreParams for testing purposes.

    Returns:
        FeatureStoreParams: An instance of FeatureStoreParams initialized with dummy data.
    """
    return FeatureStoreParams(
        feast_config_bucket="feast_config_bucket",
        config_file="feature_store.yaml",
        local_config_dir="local-config-dir",
        redshift_database="redshift_database",
        redshift_schema="feastredshift_schema",
        redshift_table="redshift_table",
        redshift_timestamp_field="event_timestamp",
    )  # Provide appropriate parameters
