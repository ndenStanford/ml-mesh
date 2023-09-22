"""Test resgister features method."""
# Standard Library
from unittest.mock import Mock, patch

# 3rd party libraries
import pytest

# Source
from src.register_features import register


@pytest.fixture
def mock_feature_store_handle():
    """Mock feature store handle."""
    return Mock()


@pytest.fixture
def mock_redshift_source_custom():
    """Mock custom redshift source."""
    return Mock()


@pytest.fixture
def mock_entity():
    """Mock feast entity."""
    return Mock()


@pytest.fixture
def mock_feature_view():
    """Mock feast feature view."""
    return Mock()


@patch("src.register_features.FeatureStoreHandle", autospec=True)
@patch("src.register_features.RedshiftSourceCustom", autospec=True)
@patch("src.register_features.Entity", autospec=True)
@patch("src.register_features.FeatureView", autospec=True)
def test_register(
    mock_feature_view,
    mock_entity,
    mock_redshift_source_custom,
    mock_feature_store_handle,
):
    """Test resgister features method."""
    # Mock the constructor of FeatureStoreHandle and other dependencies
    mock_feature_store_handle.return_value = mock_feature_store_handle
    mock_redshift_source_custom.return_value = mock_redshift_source_custom
    mock_entity.return_value = mock_entity
    mock_feature_view.return_value = mock_feature_view
    # Call the register function
    register()
    # Assertions to check if the register function calls were made with the expected arguments
    mock_feature_store_handle.assert_called_once_with(
        feast_config_bucket="kubeflow-feast-config-dev",
        config_file="feature_store.yaml",
        local_config_dir="local-config-dir",
    )

    mock_redshift_source_custom.assert_called_once_with(
        table="iptc",
        timestamp_field="event_timestamp",
        database="sources",
        schema="feast",
    )

    mock_entity.assert_called_once_with(
        name="iptc",
        join_keys=["iptc_id"],
    )
    # Additional assertions
    assert mock_feature_store_handle.register.call_count == 2
    assert mock_feature_store_handle.register.call_args_list[0][0][0] == [mock_entity]
    assert mock_feature_store_handle.register.call_args_list[1][0][0] == [
        mock_feature_view
    ]
