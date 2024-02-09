"""Class for training and managing Onclusive models."""

# Standard Library
import io
from abc import ABC, abstractmethod
from io import BytesIO

# 3rd party libraries
import boto3
from botocore.client import BaseClient

# Internal libraries
from onclusiveml.core.logging import get_default_logger
from onclusiveml.core.optimization import OnclusiveModelOptimizer
from onclusiveml.data.feature_store import (
    FeatureStoreHandle,
    FeatureStoreParams,
)
from onclusiveml.tracking import TrackedModelCard, TrackedModelSpecs


class OnclusiveModelTrainer(ABC, OnclusiveModelOptimizer):
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
        self.data_fetch_params = data_fetch_params
        self.logger = get_default_logger(__name__)

        super().__init__(
            tracked_model_specs=tracked_model_specs,
            model_card=model_card,
        )

    @abstractmethod
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
        self.get_featurestore_handle()
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

        self.dataset_df = self.fs_handle.fetch_historical_features(features)

        self.logger.info(
            f"fetched dataset from feature-store : \n {self.dataset_df.head()}"
        )

        self.docs = self.dataset_df["content"].apply(str).values.tolist()

    def get_featurestore_handle(self) -> None:
        """Initialize feature store handle for the trainer class.

        Returns: None
        """
        if self.data_fetch_params.save_artifact:
            num_samples = str(self.data_fetch_params.n_records_full)
        else:
            num_samples = str(self.data_fetch_params.n_records_sample)

        self.logger.info(f"fetching {num_samples} samples from feature-store")

        self.fs_handle = FeatureStoreHandle(
            feast_config_bucket=self.data_fetch_params.feast_config_bucket,
            config_file=self.data_fetch_params.config_file,
            local_config_dir=self.data_fetch_params.local_config_dir,
            data_source=self.data_fetch_params.redshift_table,
            data_id_key=self.data_fetch_params.entity_join_key,
            limit=num_samples,
        )

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

    @abstractmethod
    def train(self) -> None:
        """Train the model.

        Returns: None
        """
        pass

    @abstractmethod
    def predict(self) -> None:
        """Make predictions using the trained model.

        Returns: None
        """
        pass

    def __call__(self) -> None:
        """Call Method."""
        self.get_training_data()
        self.upload_training_data_to_s3()
