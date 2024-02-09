# Standard Library
from unittest.mock import patch

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
from onclusiveml.training import BertopicTrainer


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
def tracked_model_specs():
    return TrackedModelSpecs(
        project="project", model="model", api_token="api_token"
    )  # Provide appropriate parameters


@pytest.fixture
def tracked_model_card():
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
def feature_store_params():
    return FeatureStoreParams(
        feast_config_bucket="feast_config_bucket",
        config_file="feature_store.yaml",
        local_config_dir="local-config-dir",
        redshift_database="redshift_database",
        redshift_schema="feastredshift_schema",
        redshift_table="redshift_table",
        redshift_timestamp_field="event_timestamp",
    )  # Provide appropriate parameters


@pytest.fixture
@patch(
    "onclusiveml.core.optimization.OnclusiveModelOptimizer.create_tracked_model_version",
    return_value=None,
)
def bertopic_trainer(
    mock_create_tracked_model_version,
    tracked_model_specs,
    tracked_model_card,
    feature_store_params,
):
    stopwords = ["a", "an", "the"]
    bertopic_trainer = BertopicTrainer(
        tracked_model_specs=tracked_model_specs,
        model_card=tracked_model_card,
        data_fetch_params=feature_store_params,
        stopwords=stopwords,
    )
    mock_create_tracked_model_version.assert_called_once()
    return bertopic_trainer


def test_bertopic_trainer_init(
    bertopic_trainer, tracked_model_specs, tracked_model_card, feature_store_params
):
    assert bertopic_trainer.tracked_model_specs == tracked_model_specs
    assert bertopic_trainer.model_card == tracked_model_card
    assert bertopic_trainer.data_fetch_params == feature_store_params
    assert bertopic_trainer.stopwords == ["a", "an", "the"]
