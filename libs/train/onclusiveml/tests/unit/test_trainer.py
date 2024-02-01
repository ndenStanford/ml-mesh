# Standard Library
from unittest.mock import MagicMock, patch

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


@patch("onclusiveml.train.onclusive_model_trainer.FeatureStoreHandle")
@patch("onclusiveml.train.onclusive_model_trainer.boto3.client")
def test_onclusive_model_trainer_initialize_model(
    mock_boto3_client,
    mock_feature_store_handle,
    tracked_model_specs,
    tracked_model_card,
    feature_store_params,
):
    trainer = OnclusiveModelTrainer(
        tracked_model_specs, tracked_model_card, feature_store_params
    )
    trainer.initialize_model()
    # Ensure FeatureStoreHandle is initialized with the correct parameters
    mock_feature_store_handle.assert_called_once_with(
        feast_config_bucket=feature_store_params.feast_config_bucket,
        config_file=feature_store_params.config_file,
        local_config_dir=feature_store_params.local_config_dir,
        data_source=feature_store_params.redshift_table,
        data_id_key=feature_store_params.entity_join_key,
        limit=feature_store_params.limit,
    )


@patch("onclusiveml.train.onclusive_model_trainer.FeatureStoreHandle")
@patch("onclusiveml.train.onclusive_model_trainer.boto3.client")
def test_onclusive_model_trainer_get_training_data(
    mock_boto3_client,
    mock_feature_store_handle,
    tracked_model_specs,
    tracked_model_card,
    feature_store_params,
):
    trainer = OnclusiveModelTrainer(
        tracked_model_specs, tracked_model_card, feature_store_params
    )
    # Mocking FeatureStoreHandle.list_entities, list_data_sources, and list_feature_views
    mock_feature_store_handle.return_value.list_entities.return_value = [
        MagicMock(name="entity1"),
        MagicMock(name="entity2"),
    ]
    mock_feature_store_handle.return_value.list_data_sources.return_value = [
        MagicMock(name="datasource1"),
        MagicMock(name="datasource2"),
    ]
    mock_feature_store_handle.return_value.list_feature_views.return_value = [
        MagicMock(name="feature_view1"),
        MagicMock(name="feature_view2"),
    ]
    # Mocking FeatureStoreHandle.fetch_historical_features
    mock_feature_store_handle.return_value.fetch_historical_features.return_value = (
        pd.DataFrame(...)
    )  # Provide appropriate DataFrame

    trainer.get_training_data()
    # Ensure FeatureStoreHandle methods are called as expected
    mock_feature_store_handle.return_value.list_entities.assert_called_once()
    mock_feature_store_handle.return_value.list_data_sources.assert_called_once()
    mock_feature_store_handle.return_value.list_feature_views.assert_called_once()
    mock_feature_store_handle.return_value.fetch_historical_features.assert_called_once()


@patch("onclusiveml.train.onclusive_model_trainer.boto3.client")
@patch("onclusiveml.train.onclusive_model_trainer.s3_parquet_upload")
def test_onclusive_model_trainer_upload_training_data_to_s3(
    mock_s3_parquet_upload,
    mock_boto3_client,
    tracked_model_specs,
    tracked_model_card,
    feature_store_params,
):
    trainer = OnclusiveModelTrainer(
        tracked_model_specs, tracked_model_card, feature_store_params
    )
    # Mocking s3_parquet_upload
    mock_s3_parquet_upload.return_value = "test/file/key.parquet"

    trainer.upload_training_data_to_s3()
    # Ensure s3_parquet_upload is called with the correct parameters
    mock_s3_parquet_upload.assert_called_once_with(
        client=mock_boto3_client.return_value,
        file_key="test/file/key.parquet",
        parquet_buffer=MagicMock(),
    )
