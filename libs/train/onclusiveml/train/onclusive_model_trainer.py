"""Class for training and managing Onclusive models."""

# Standard Library
import io
from io import BytesIO
from typing import List

# 3rd party libraries
import boto3
from botocore.client import BaseClient

# Internal libraries
from onclusiveml.core.logging import get_default_logger
from onclusiveml.data.feature_store import (
    FeatureStoreHandle,
    FeatureStoreParams,
)
from onclusiveml.tracking import (
    TrackedModelCard,
    TrackedModelSpecs,
    TrackedModelVersion,
)


class OnclusiveModelTrainer:
    """Class for training and managing Onclusive models."""

    def __init__(
        self,
        tracked_model_specs: TrackedModelSpecs,
        model_card: TrackedModelCard,
        data_fetch_params: FeatureStoreParams,
    ) -> None:
        """Initialize the OnclusiveModelTrainer.

        Args:
            tracked_model_specs (TrackedModelSpecs): Specifications for tracked model on neptune.
            model_card (TrackedModelCard): Model card with specifications of the model.
            data_fetch_params (FeatureStoreParams): Parameters for fetching data from feature store.

        Returns: None
        """
        self.tracked_model_specs = tracked_model_specs
        self.model_card = model_card
        self.tracked_model_version = TrackedModelVersion(
            **self.tracked_model_specs.dict()
        )
        self.data_fetch_params = data_fetch_params

        self.logger = get_default_logger(__name__)

    def initialize_model(self) -> None:
        """Initialize the model.

        Returns: None
        """
        pass

    def get_training_data(self) -> None:
        """Fetch and prepare training data from the feature store.

        Returns: None
        """
        self.logger.info("initializing feature-store handle...")
        self.fs_handle = FeatureStoreHandle(
            feast_config_bucket=self.data_fetch_params.feast_config_bucket,
            config_file=self.data_fetch_params.config_file,
            local_config_dir=self.data_fetch_params.local_config_dir,
            data_source=self.data_fetch_params.redshift_table,
            data_id_key=self.data_fetch_params.entity_join_key,
            limit=self.data_fetch_params.limit,
        )
        self.logger.info(
            f"Registered entities: {[entity.name for entity in self.fs_handle.list_entities()]}"
        )
        self.logger.info(
            f"Registered datasources: "
            f"{[datasource.name for datasource in self.fs_handle.list_data_sources()]}"
        )
        self.logger.info(
            f"Registered feature views: "
            f"{[feature_view.projection.name for feature_view in self.fs_handle.list_feature_views()]}"  # noqa: E501
        )
        self.feature_view = [
            feature_view
            for feature_view in self.fs_handle.list_feature_views()
            if feature_view.name == self.data_fetch_params.feature_view_name
        ][0]

        features = [
            f"{self.feature_view.name}:{feature.name}"
            for feature in self.feature_view.features
        ]

        self.logger.info(
            f"fetching {self.data_fetch_params.limit} samples from feature-store"
        )

        self.dataset_df = self.fs_handle.fetch_historical_features(features)

        self.logger.info(
            f"fetched dataset from feature-store : \n {self.dataset_df.head()}"
        )

        self.docs = self.dataset_df["content"].apply(str).values.tolist()

    def upload_training_data_to_s3(self) -> None:
        """Upload the training dataset to S3.

        Returns: None
        """
        self.client = boto3.client("s3")
        parquet_buffer = io.BytesIO()
        self.dataset_df.to_parquet(parquet_buffer, index=False)
        file_name = self.tracked_model_version.get_url().split("/")[-1]

        file_key = f"{self.data_fetch_params.dataset_upload_dir}/{file_name}.parquet"
        full_file_key = self.s3_parquet_upload(
            self.client,
            file_key,
            parquet_buffer,
            self.data_fetch_params.dataset_upload_bucket,
        )
        self.full_file_key = full_file_key

    @staticmethod
    def s3_parquet_upload(
        client: BaseClient, file_key: str, parquet_buffer: BytesIO, s3_bucket: str
    ) -> str:
        """Put object to S3 bucket.

        Args:
            client (BaseClient): Boto3 S3 client.
            file_key (str): Path of the uploaded file.
            parquet_buffer (BytesIO): Buffer containing Parquet data.
            s3_bucket (str): S3 bucket for uploading dataset file.

        Returns:
            str: Full S3 key for the uploaded dataset file.
        """
        parquet_buffer.seek(0)
        client.put_object(
            Body=parquet_buffer.getvalue(),
            Bucket=s3_bucket,
            Key=file_key,
        )

        return f"{s3_bucket}/{file_key}"

    def train(self) -> None:
        """Train the model.

        Returns: None
        """
        pass

    def predict(self) -> None:
        """Make predictions using the trained model.

        Returns: None
        """
        pass

    def upload_model_to_neptune(
        self,
        test_files: List,
        test_file_attribute_paths: List,
        model_local_directory: str,
    ) -> None:
        """Upload model-related information to Neptune.

        Args:
            test_files (List): List of test files.
            test_file_attribute_paths (List): List of attribute paths for test files.
            model_local_directory (str): Local directory path with the saved model.

        Returns: None
        """
        for (test_file, test_file_attribute_path) in zip(
            test_files, test_file_attribute_paths
        ):
            self.tracked_model_version.upload_config_to_model_version(
                config=test_file, neptune_attribute_path=test_file_attribute_path
            )

        self.tracked_model_version.upload_directory_to_model_version(
            local_directory_path=model_local_directory,
            neptune_attribute_path=self.model_card.model_artifact_attribute_path,
        )
        # # model card
        self.tracked_model_version.upload_config_to_model_version(
            config=self.model_card.dict(), neptune_attribute_path="model/model_card"
        )
        self.tracked_model_version.stop()
