"""Fetch features and upload a dataset version."""

# Standard Library
import io
from io import BytesIO
from typing import Any

# 3rd party libraries
import boto3
from botocore.client import BaseClient

# Internal libraries
from onclusiveml.core.logging import get_default_logger
from onclusiveml.data.feature_store import FeatureStoreHandle

# Source
from src.settings import DataFetchParams  # type: ignore[attr-defined]


logger = get_default_logger(__name__)


def upload(object_to_upload: Any, file_name: str) -> str:
    """Upload a dataset version.

    Attributes:
        object_to_upload (Any): dataset object to be uploaded.
        file_name (str): name to be given to uploaded file.
    """
    data_fetch_params = DataFetchParams()
    client = boto3.client("s3")
    parquet_buffer = io.BytesIO()
    try:
        object_to_upload.to_parquet(parquet_buffer, index=False)
        file_key = f"{data_fetch_params.dataset_upload_dir}/{file_name}.parquet"
        full_file_key = s3_put(client, file_key, parquet_buffer)
    except Exception as e:
        logger.info(
            f"Unable to upload full dataset. Uploading a sample. Cause: {str(e)}"
        )
        object_to_upload.sample(500).to_parquet(parquet_buffer, index=False)
        file_key = f"{data_fetch_params.dataset_upload_dir}/{file_name}_sample.parquet"
        full_file_key = s3_put(client, file_key, parquet_buffer)
    return full_file_key


def s3_put(client: BaseClient, file_key: str, parquet_buffer: BytesIO) -> str:
    """Put object to S3 bucket.

    Args:
        client (BaseClient): Boto3 S3 client.
        file_key (str): Path of the uploaded file.
        parquet_buffer (BytesIO): Buffer containing Parquet data.

    Returns:
        str: The key of the uploaded file.
    """
    data_fetch_params = DataFetchParams()
    parquet_buffer.seek(0)
    client.put_object(
        Body=parquet_buffer.getvalue(),
        Bucket=data_fetch_params.dataset_upload_bucket,
        Key=file_key,
    )
    return file_key


def fetch_and_upload(file_name: str) -> Any:
    """Fetch from feature store and upload to s3."""
    data_fetch_params = DataFetchParams()
    logger.info("initializing feature-store handle...")
    fs_handle = FeatureStoreHandle(
        feast_config_bucket=data_fetch_params.feast_config_bucket,
        config_file=data_fetch_params.config_file,
        local_config_dir=data_fetch_params.local_config_dir,
        data_source=data_fetch_params.redshift_table,
        data_id_key=data_fetch_params.entity_join_key,
        limit=data_fetch_params.limit,
    )
    logger.info(
        f"Registered entities: {[entity.name for entity in fs_handle.list_entities()]}"
    )
    logger.info(
        f"Registered datasources: "
        f"{[datasource.name for datasource in fs_handle.list_data_sources()]}"
    )
    logger.info(
        f"Registered feature views: "
        f"{[feature_view.projection.name for feature_view in fs_handle.list_feature_views()]}"
    )
    feature_view = [
        feature_view
        for feature_view in fs_handle.list_feature_views()
        if feature_view.name == data_fetch_params.feature_view_name
    ][0]
    features = [
        f"{feature_view.name}:{feature.name}" for feature in feature_view.features
    ]
    dataset_df = fs_handle.fetch_historical_features(features)
    file_key = upload(dataset_df, file_name)
    logger.info(f"{dataset_df.shape[0]} samples pulled from feature store.")
    return dataset_df, file_key
