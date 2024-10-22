"""Class for training and managing Onclusive models."""

# Standard Library
import io
from abc import abstractmethod
from io import BytesIO

# 3rd party libraries
import boto3
from botocore.client import BaseClient

# Internal libraries
from onclusiveml.core.logging import get_default_logger
from onclusiveml.feature_store.feast import FeastFeatureStore
from onclusiveml.feature_store.settings import FeastFeatureStoreSettings
from onclusiveml.tracking import TrackedModelCard, TrackedModelSettings
from onclusiveml.tracking.optimization import OnclusiveModelOptimizer


class OnclusiveModelTrainer(OnclusiveModelOptimizer):
    """Class for training and managing Onclusive models."""

    def __init__(
        self,
        tracked_model_specs: TrackedModelSettings,
        model_card: TrackedModelCard,
        settings: FeastFeatureStoreSettings,
    ) -> None:
        """Initialize the OnclusiveModelTrainer.

        Args:
            tracked_model_specs (TrackedModelSettings): Specifications for tracked model on neptune.
            model_card (TrackedModelCard): Model card with specifications of the model.
            settings (FeatureStoreParams): Parameters for fetching data from feature store.

        Returns: None
        """
        self.data_fetch_params = settings
        self.logger = get_default_logger(__name__)

        super().__init__(
            tracked_model_settings=tracked_model_specs,
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
        self.logger.info("initializing feature-store...")
        self.get_featurestore()

        if self.num_samples != "-1":
            entity_df = self.data_fetch_params.entity_df + f" LIMIT {self.num_samples}"

        self.dataset_df = self.fs.get_historical_features(
            entity_df=entity_df,
            features=self.data_fetch_params.features,
        )
        self.logger.info(
            f"fetched dataset from feature-store : \n {self.dataset_df.head()}"
        )

        self.docs = self.dataset_df["content"].apply(str).values.tolist()

    def get_featurestore(self) -> None:
        """Initialize feature store for the trainer class.

        Returns: None
        """
        if self.data_fetch_params.save_artifact:
            self.num_samples = str(self.data_fetch_params.n_records_full)
        else:
            self.num_samples = str(self.data_fetch_params.n_records_sample)

        self.logger.info(f"fetching {self.num_samples} samples from feature-store")

        self.fs = FeastFeatureStore.from_settings(self.data_fetch_params)

    def upload_training_data_to_s3(self) -> None:
        """Upload the training dataset to S3.

        Returns: None
        """
        self.client = boto3.client("s3")
        self.parquet_buffer = io.BytesIO()
        self.dataset_df.to_parquet(self.parquet_buffer, index=False)

        s3_bucket = self.data_fetch_params.dataset_upload_bucket
        # assemble full s3 uri for file
        s3_model_version_full_prefix = (
            self.tracked_model_version.derive_model_version_s3_prefix()
        )
        s3_model_version_prefix = "/".join(s3_model_version_full_prefix.split("/")[-3:])

        file_name = self.tracked_model_version.get_url().split("/")[-1] + ".parquet"
        self.neptune_attr_path = (
            f"{self.model_card.training_data_attribute_path}/{file_name}"
        )

        file_key = (
            f"{self.data_fetch_params.dataset_upload_dir}/"
            f"{s3_model_version_prefix}/{self.neptune_attr_path}"
        )
        full_file_key = self.s3_parquet_upload(
            self.client,
            file_key,
            self.parquet_buffer,
            s3_bucket,
        )
        self.full_file_key = full_file_key

        if self.data_fetch_params.save_artifact:
            self.track_training_data_in_neptune()

    def track_training_data_in_neptune(self) -> None:
        """Set up tracking of training data S3 file in Neptune.

        Returns: None
        """
        self.tracked_model_version[self.neptune_attr_path].track_files(
            f"s3://{self.full_file_key}"
        )

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

    def optimize_model(self) -> None:
        """Optimize the model.

        Returns: None
        """
        self.train()

    def __call__(self) -> None:
        """Call Method."""
        self.get_training_data()
        self.upload_training_data_to_s3()
