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
from onclusiveml.data.feature_store import (
    FeatureStoreHandle,
    FeatureStoreParams,
)
from onclusiveml.tracking import TrackedModelCard, TrackedModelSettings
from onclusiveml.tracking.optimization import OnclusiveModelOptimizer


class OnclusiveModelTrainer(OnclusiveModelOptimizer):
    """Class for training and managing Onclusive models."""

    def __init__(
        self,
        tracked_model_specs: TrackedModelSettings,
        model_card: TrackedModelCard,
        data_fetch_params: FeatureStoreParams,
    ) -> None:
        """Initialize the OnclusiveModelTrainer.

        Args:
            tracked_model_specs (TrackedModelSettings): Specifications for tracked model on neptune.
            model_card (TrackedModelCard): Model card with specifications of the model.
            data_fetch_params (FeatureStoreParams): Parameters for fetching data from feature store.

        Returns: None
        """
        self.data_fetch_params = data_fetch_params
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

        base_feature_view_name = self.data_fetch_params.feature_view_name
        for feature_view in self.fs_handle.list_feature_views():
            self.logger.info(f"XXXXXXXXX{feature_view}xXXXXXXX")
        for feature_view in self.fs_handle.list_on_demand_feature_views():
            self.logger.info(f"DDDDDDDDD{feature_view}DDDDDDDD")
        self.feature_view = [
            feature_view
            for feature_view in self.fs_handle.list_feature_views()
            if feature_view.name == base_feature_view_name
        ][0]

        features = [
            f"{self.feature_view.name}:{feature.name}"
            for feature in self.feature_view.features
        ]

        # If the dataset is on-demand, add the corresponding on-demand features
        # if self.data_fetch_params.is_on_demand:
        #     on_demand_feature_view = [
        #         feature_view
        #         for feature_view in self.fs_handle.list_on_demand_feature_views()
        #         if feature_view.name == f"{base_feature_view_name}_on_demand"
        #     ][0]

        #     on_demand_features = [
        #         f"{on_demand_feature_view.name}:{feature.name}"
        #         for feature in on_demand_feature_view.features
        #     ]
        #     features.extend(on_demand_features)
        #     self.logger.info(f"Added on-demand features: {on_demand_features}")
        features += ["iptc_first_level_on_demand_feature_view:topic_2_llm"]
        self.dataset_df = self.fs_handle.fetch_historical_features(
            features,
            filter_columns=self.data_fetch_params.filter_columns,
            filter_values=self.data_fetch_params.filter_values,
            comparison_operators=self.data_fetch_params.comparison_operators,
            non_nullable_columns=self.data_fetch_params.non_nullable_columns,
        )
        self.logger.info(self.dataset_df.head())
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
