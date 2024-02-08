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
)
from onclusiveml.train.onclusive_model_trainer import OnclusiveModelTrainer


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


@pytest.fixture
def feature_store_params():
    return FeatureStoreParams(
        feast_config_bucket="feast_config_bucket",
        config_file="feature_store.yaml",
        local_config_dir="local-config-dir",
        redshift_database="redshift_database",
        redshift_schema="feasredshift_schemat",
        redshift_table="redshift_table",
        redshift_timestamp_field="event_timestamp",
    )  # Provide appropriate parameters


@patch(
    "onclusiveml.core.optimization.OnclusiveModelOptimizer.set_tracked_model_version"
)
def test_onclusive_model_trainer_initialize(
    mock_set_tracked_model_version,
    tracked_model_specs,
    tracked_model_card,
    feature_store_params,
):
    mock_set_tracked_model_version.return_value = (
        None  # Prevent the original method from being called
    )
    trainer = OnclusiveModelTrainer(
        tracked_model_specs, tracked_model_card, feature_store_params
    )
    assert trainer.tracked_model_specs == tracked_model_specs
    assert trainer.model_card == tracked_model_card
    assert trainer.data_fetch_params == feature_store_params
    mock_set_tracked_model_version.assert_called_once()
