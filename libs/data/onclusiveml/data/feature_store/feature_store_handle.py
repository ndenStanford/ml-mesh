"""Handle for feast feature store."""

# Standard Library
import os
from typing import List, Optional

# 3rd party libraries
import boto3
import botocore
from boto3_type_annotations.s3 import Client
from feast import FeatureStore
from feast.data_source import DataSource
from feast.feast_object import FeastObject


class FeatureStoreHandle:
    """Handle for feast feature store.

    Attributes:
        feast_config_bucket (str): S3 bucket that stores feast-config yaml.
        config_file (str): Name of the feast-config yaml.
        local_config_dir (str): Name of the local directory to store the feast-config yaml.
        s3_handle (Client): S3 client for interacting with the bucket.
    """

    def __init__(
        self,
        feast_config_bucket: Optional[str] = "kubeflow-feast-config-prod",
        config_file: Optional[str] = "feature_store.yaml",
        local_config_dir: str = "feature_config",
        s3_handle: Client = None,
    ):

        self.feast_config_bucket = feast_config_bucket
        self.config_file = config_file
        self.local_config_dir = local_config_dir

        if s3_handle is None:
            self.s3_handle = boto3.resource("s3")
        else:
            self.s3_handle = s3_handle

        self.config_file_path = self.s3_config_downloader()
        self.initialize()

    def initialize(self) -> None:
        """Initializes feature store registry.

        Returns: None

        """
        self.fs = FeatureStore(fs_yaml_file=self.config_file_path)
        self.fs.apply([])

    def s3_config_downloader(self) -> str:
        """Downloads feast-config yaml from s3 in local directory.

        Returns: Path of the local feast-config yaml.

        """
        if not os.path.exists(self.local_config_dir):
            os.makedirs(self.local_config_dir)

        try:
            self.s3_handle.Bucket(self.feast_config_bucket).download_file(
                self.config_file, f"{self.local_config_dir}/{self.config_file}"
            )
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "404":
                print("The object does not exist.")
            else:
                raise
        return f"{self.local_config_dir}/{self.config_file}"

    def register(self, components: List[FeastObject]) -> None:
        """Registers feast components.

        Args:
            components (List[FeastObject]): List of feast components to register.

        Returns: None

        """
        self.fs.apply(components)

    def delete(self, components: List[FeastObject]) -> None:
        """Deletes feast components.

        Args:
            components (List[FeastObject]): List of feast components to delete.

        Returns: None

        """
        self.fs.apply(objects_to_delete=components, partial=False)

    def list_entities(self) -> List[FeastObject]:
        """Lists feast entites.

        Returns: List of entities registered with feast.

        """
        return self.fs.list_entities()

    def list_feature_views(self) -> List[FeastObject]:
        """Lists feast feature views.

        Returns: List of feature views registered with feast.

        """
        return self.fs.list_feature_views()

    def list_data_sources(self) -> List[FeastObject]:
        """Lists feast data sources.

        Returns: List of data sources registered with feast.

        """
        return self.fs.list_data_sources()

    def redshift_entity_df_query_builder(self) -> None:
        """Builds redshift query for entity dataframe.

        Returns: None

        """
        self.entity_sql = f"""
                SELECT
                    {self.version_key}, event_timestamp
                FROM {self.fs.get_data_source({self.data_source}).get_table_query_string()}
                WHERE {self.version_key} in {self.dataset_versions}
            """

    def fetch_historical_features(
        self,
        features: List[str],
        data_source: DataSource,
        version_key: str = "dataset_version",
        dataset_versions: str = "v1",
    ) -> None:
        """Fetches Historical features from feast feature store.

        Args:
            features (List[str): List of features to fetch from feast.
            data_source (DataSource): Name of the datasource to fetch features from.
            version_key (str): Name of the field that records dataset version.
            dataset_versions (str): List of dataset versions to fetch.


        Returns: Pandas dataframe with historical features.

        """
        self.data_source = data_source
        self.version_key = version_key
        self.dataset_versions = dataset_versions
        self.redshift_entity_df_query_builder()
        return self.fs.get_historical_features(
            entity_df=self.entity_sql,
            features=features,
        ).to_df()