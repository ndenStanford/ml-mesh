"""FeatureStoreHandle test."""

# Standard Library
import os

# 3rd party libraries
import boto3
import pytest
from moto import mock_s3

# Internal libraries
from onclusiveml.data.feature_store.feature_store_handle import (
    FeatureStoreHandle,
)


@pytest.fixture
@mock_s3
def feature_store_handle_instance(mocker):
    """Define a fixture for creating a patched instance of the FeatureStoreHandle class.

    Args:
        mocker: pytest-mock based mocker object to create mock objects.

    Returns: Patched instance of FeatureStoreHandle class.

    """
    mock_feature_store = mocker.Mock()
    mocker.patch(
        "onclusiveml.data.feature_store.feature_store_handle.FeatureStore",
        return_value=mock_feature_store,
    )
    mocker.patch(
        "onclusiveml.data.feature_store.feature_store_handle.FeatureStore.apply",
        return_value=None,
    )
    mocker.patch(
        "onclusiveml.data.feature_store.feature_store_handle.FeatureStore.list_entities",
        return_value=None,
    )
    mocker.patch(
        "onclusiveml.data.feature_store.feature_store_handle.FeatureStore.list_feature_views",
        return_value=None,
    )
    mocker.patch(
        "onclusiveml.data.feature_store.feature_store_handle.FeatureStore.list_data_sources",
        return_value=None,
    )
    mocker.patch(
        "onclusiveml.data.feature_store.feature_store_handle.FeatureStore.get_historical_features",
        return_value=None,
    )

    s3_handle = boto3.resource("s3")
    s3_handle.create_bucket(Bucket="test-bucket")
    test_object = s3_handle.Object("test-bucket", "test-config.yaml")
    test_object.put(Body="")

    return FeatureStoreHandle(
        feast_config_bucket="test-bucket",
        config_file="test-config.yaml",
        local_config_dir="test-config-dir",
        s3_handle=s3_handle,
        data_source="test_data_source",
        data_id_key="entity_key",
        data_ids=["1", "2"],
    )


def test_feature_store_handle_initialization(feature_store_handle_instance):
    """Test the initialization of the FeatureStoreHandle class.

    Args:
        feature_store_handle_instance: Patched instance of FeatureStoreHandle class.

    Returns: None

    """
    assert feature_store_handle_instance.feast_config_bucket == "test-bucket"
    assert feature_store_handle_instance.config_file == "test-config.yaml"
    assert feature_store_handle_instance.local_config_dir == "test-config-dir"
    assert os.path.exists(feature_store_handle_instance.config_file_path)
    assert feature_store_handle_instance.data_source == "test_data_source"
    assert feature_store_handle_instance.data_id_key == "entity_key"
    assert feature_store_handle_instance.data_ids == ["1", "2"]
    feature_store_handle_instance.fs.apply.assert_called_once_with([])


def test_register(feature_store_handle_instance, mocker):
    """Test register method.

    Args:
        feature_store_handle_instance: Patched instance of FeatureStoreHandle class.
        mocker: pytest-mock based mocker object to create mock objects.

    Returns: None

    """
    # Create a mock FeastObject
    mock_feast_object = mocker.Mock()
    # Call the register method
    feature_store_handle_instance.register([mock_feast_object])
    # Assert that the apply method of the Feast Feature Store was called with the mock FeastObject
    feature_store_handle_instance.fs.apply.assert_called_with([mock_feast_object])


def test_delete(feature_store_handle_instance, mocker):
    """Test delete method.

    Args:
        feature_store_handle_instance: Patched instance of FeatureStoreHandle class.
        mocker: pytest-mock based mocker object to create mock objects.

    Returns: None

    """
    # Create a mock FeastObject
    mock_feast_object = mocker.Mock()
    # Call the delete method
    feature_store_handle_instance.delete([mock_feast_object])
    # Assert that the apply method of the Feast Feature Store
    feature_store_handle_instance.fs.apply.assert_called_with(
        [], objects_to_delete=[mock_feast_object], partial=False
    )


def test_list_entities(feature_store_handle_instance):
    """Test list_entities method.

    Args:
        feature_store_handle_instance: Patched instance of FeatureStoreHandle class.

    Returns: None

    """
    # Call the list_entities method
    feature_store_handle_instance.list_entities()

    feature_store_handle_instance.fs.list_entities.assert_called_with()


def test_list_feature_views(feature_store_handle_instance):
    """Test list_feature_views method.

    Args:
        feature_store_handle_instance: Patched instance of FeatureStoreHandle class.

    Returns: None

    """
    # Call the list_feature_views method
    feature_store_handle_instance.list_feature_views()

    feature_store_handle_instance.fs.list_feature_views.assert_called_with()


def test_list_data_sources(feature_store_handle_instance):
    """Test list_data_sources method.

    Args:
        feature_store_handle_instance: Patched instance of FeatureStoreHandle class.

    Returns: None

    """
    # Call the list_data_sources method
    feature_store_handle_instance.list_data_sources()

    feature_store_handle_instance.fs.list_data_sources.assert_called_with()


def test_fetch_historical_features(feature_store_handle_instance):
    """Test list_data_sources method.

    Args:
        feature_store_handle_instance: Patched instance of FeatureStoreHandle class.

    Returns: None

    """
    # Call the fetch_historical_features method
    feature_store_handle_instance.fetch_historical_features()
    feature_store_handle_instance.fs.get_historical_features.assert_called_once()
