"""Handle for feast feature store."""

# Standard Library
import os
from typing import Any, List, Optional

# 3rd party libraries
import boto3
import botocore
import pandas as pd
import yaml
from boto3_type_annotations.s3 import Client
from feast import Entity, FeatureStore, FeatureView
from feast.data_source import DataSource
from feast.feast_object import FeastObject
from feast.feature_store import RepoContents

# Internal libraries
from onclusiveml.core.logging import get_default_logger


class FeatureStoreHandle:
    """Handle for feast feature store.

    Attributes:
        feast_config_bucket (str): S3 bucket that stores feast-config yaml.
        config_file (str): Name of the feast-config yaml.
        local_config_dir (str): Name of the local directory to store the feast-config yaml.
        s3_handle (Client): S3 client for interacting with the bucket.
        features (List[str): List of features to fetch from feast.
        data_source (DataSource): Name of the datasource to fetch features from.
        data_id_key (str): Name of the field that records data ids.
        data_ids (str): List of data ids to fetch.

    """

    def __init__(
        self,
        feast_config_bucket: Optional[str] = "kubeflow-feast-config-prod",
        config_file: Optional[str] = "feature_store.yaml",
        local_config_dir: str = "feature_config",
        s3_handle: Client = None,
        data_source: DataSource = None,
        data_id_key: str = "entity_key",
        data_ids: List[str] = ["1", "2"],
        limit: str = "1000",
        timestamp_key: str = "event_timestamp",
    ):

        self.logger = get_default_logger(__name__)

        self.feast_config_bucket = feast_config_bucket
        self.config_file = config_file
        self.local_config_dir = local_config_dir

        if s3_handle is None:
            self.s3_handle = boto3.resource("s3")
        else:
            self.s3_handle = s3_handle

        self.config_file_path = self.s3_config_downloader()

        self.initialize()

        self.data_source = data_source
        self.data_id_key = data_id_key
        self.data_ids = data_ids
        self.limit = limit
        self.timestamp_key = timestamp_key
        self.operator_dict = {
            "equal": "=",
            "less_than": "<",
            "greater_than": ">",
            "less_than_equal_to": "<=",
            "greater_than_equal_to": ">=",
        }

    def initialize(self) -> None:
        """Initializes feature store registry.

        Returns: None

        """
        self.fs = FeatureStore(fs_yaml_file=self.config_file_path)
        self.fs.apply([])

    def update_yaml_database(self, yaml_file_path: str):
        """Updates the database in the YAML file after downloading.

        Args:
            yaml_file_path (str): The path of the downloaded YAML file.
        """
        with open(yaml_file_path, "r") as file:
            config = yaml.safe_load(file)
        # Update the database field
        config["offline_store"]["database"] = "warehouse"

        with open(yaml_file_path, "w") as file:
            yaml.safe_dump(config, file, default_flow_style=False)

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
            self.update_yaml_database(f"{self.local_config_dir}/{self.config_file}")
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

    def plan(
        self,
        data_sources: List[DataSource],
        feature_views: List[FeatureView],
        entities: List[Entity],
    ) -> Any:
        """Generates a plan for registering Feast components.

        This method takes lists of data sources, feature views, and entities and generates
        a plan for registering these Feast components. It creates a RepoContents object
        with the specified components and then calls the plan method of the Feast FeatureStore.

        Args:
            data_sources (List[DataSource]): List of data sources to be included in the plan.
            feature_views (List[FeatureView]): List of feature views to be included in the plan.
            entities (List[Entity]): List of entities to be included in the plan.

        Returns:
            Any: A tuple containing the
            registry difference, infrastructure difference, and new infrastructure
            generated by the plan.

        """
        repo_contents = RepoContents(
            data_sources=data_sources,
            feature_views=feature_views,
            on_demand_feature_views=list(),
            stream_feature_views=list(),
            request_feature_views=list(),
            entities=entities,
            feature_services=list(),
        )
        registry_diff, infra_diff, new_infra = self.fs.plan(
            repo_contents
        )  # register entity and feature view

        return registry_diff, infra_diff, new_infra

    def delete(self, components: List[FeastObject]) -> None:
        """Deletes feast components.

        Args:
            components (List[FeastObject]): List of feast components to delete.

        Returns: None

        """
        self.fs.apply([], objects_to_delete=components, partial=False)

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

    def list_on_demand_feature_views(self) -> List[FeastObject]:
        """Lists feast on-demand feature views.

        Returns: List of on-demand feature views registered with feast.

        """
        return self.fs.list_on_demand_feature_views()

    def list_data_sources(self) -> List[FeastObject]:
        """Lists feast data sources.

        Returns: List of data sources registered with feast.

        """
        return self.fs.list_data_sources()

    def fetch_historical_features(
        self,
        features: List[str] = ["test_feature_view:feature_1"],
        filter_columns: List[str] = [],
        filter_values: List[str] = [],
        comparison_operators: List[str] = [],
        non_nullable_columns: List[str] = [],
    ) -> pd.DataFrame:
        """Fetches Historical features from feast feature store.

        Returns: Pandas dataframe with historical features.
        """
        if len(filter_columns) != len(filter_values) or len(filter_columns) != len(
            comparison_operators
        ):
            raise ValueError(
                "Lengths of filter_columns, filter_values, \
                and comparison_operators must be the same."
            )

        self.entity_sql = f"""
                        SELECT
                            {self.data_id_key}, CURRENT_TIMESTAMP AS {self.timestamp_key} FROM
                            {self.fs.get_data_source(self.data_source).get_table_query_string()}
                    """

        if filter_columns and filter_values and comparison_operators:
            filters = []
            for column, value, operator in zip(
                filter_columns, filter_values, comparison_operators
            ):
                if operator in self.operator_dict.keys():
                    filters.append(f"{column} {self.operator_dict[operator]} '{value}'")
                else:
                    raise ValueError(
                        "Comparison operator is not valid. Should be one of the following: \
                        ['equal', 'less_than', 'greater_than', \
                        'less_than_equal_to', 'greater_than_equal_to']"
                    )

            self.entity_sql += " WHERE "
            self.entity_sql += " AND ".join(filters)
            self.entity_sql += " AND " + " AND ".join(
                f" {column} is NOT NULL"
                for column in filter_columns + non_nullable_columns
            )  # noqa: E501
        elif non_nullable_columns:
            self.entity_sql += " WHERE "
            self.entity_sql += " AND ".join(
                f" {column} is NOT NULL" for column in non_nullable_columns
            )

        if self.limit != "-1":
            self.entity_sql += f" LIMIT {self.limit}"

        self.logger.info(f"running sql query: {self.entity_sql}")

        return self.fs.get_historical_features(
            entity_df=self.entity_sql,
            features=features,
        ).to_df()
