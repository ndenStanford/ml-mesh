"""Feast feature store."""

# Standard Library
import datetime
from typing import List, Union

# 3rd party libraries
import pandas as pd
from feast import FeatureStore, RepoConfig
from feast.infra.offline_stores.redshift import (
    RedshiftOfflineStore,
    RedshiftOfflineStoreConfig,
)
from feast.infra.registry.registry import Registry
from feast.infra.registry.sql import SqlRegistryConfig
from pydantic import SecretStr

# Internal libraries
from onclusiveml.feature_store.base import BaseFeatureStore
from onclusiveml.feature_store.constants import MAX_DATETIME, MIN_DATETIME


class FeastFeatureStore(BaseFeatureStore):
    """Class to interact with the Feast feature store."""

    def __init__(
        self,
        project: str,
        mysql_host: str,
        mysql_user: str,
        mysql_port: str,
        mysql_password: SecretStr,
        redshift_cluster_id: str,
        redshift_user: str,
        redshift_cluster_region: str,
        redshift_database: str,
        redshift_s3_staging_directory: str,
        redshift_iam_role: str,
    ) -> None:
        self.project = project
        self.mysql_host = mysql_host
        self.mysql_user = mysql_user
        self.mysql_port = mysql_port
        self.mysql_password = mysql_password
        self.redshift_cluster_id = redshift_cluster_id
        self.redshift_user = redshift_user
        self.redshift_cluster_region = redshift_cluster_region
        self.redshift_database = redshift_database
        self.redshift_s3_staging_directory = redshift_s3_staging_directory
        self.redshift_iam_role = redshift_iam_role

    @property
    def repo_config(self) -> RepoConfig:
        """Feast repo."""
        registry_config = SqlRegistryConfig(
            registry_store_type="aws",
            registry_type="sql",
            path=f"mysql+pymysql://{self.mysql_user}:{self.mysql_password.get_secret_value()}@{self.mysql_host}:{self.mysql_port}/feast",
        )

        offline_store = RedshiftOfflineStoreConfig(
            cluster_id=self.redshift_cluster_id,
            user=self.redshift_user,
            region=self.redshift_cluster_region,
            database=self.redshift_database,
            s3_staging_location=self.redshift_s3_staging_directory,
            iam_role=self.redshift_iam_role,
        )

        return RepoConfig(
            project=self.project,
            provider="aws",
            registry=registry_config,
            offline_store=offline_store,
            entity_key_serialization_version=2,
        )

    @property
    def feature_store(self) -> FeatureStore:
        """Returns feature store instance."""
        return FeatureStore(config=self.repo_config)

    def get_historical_features(
        self,
        entity_df: Union[pd.DataFrame, str],
        features: List[str],
        full_feature_names: bool = False,
    ) -> pd.DataFrame:
        """Returns the historical features for training or batch scoring.

        Args:
            entity_df: The entity DataFrame or entity name.
            features: The features to retrieve.
            full_feature_names: Whether to return the full feature names.

        Returns:
            The historical features as a Pandas DataFrame.
        """
        return self.feature_store.get_historical_features(
            entity_df=entity_df,
            features=features,
            full_feature_names=full_feature_names,
        ).to_df()

    def get_training_dataset(
        self,
        name: str,
        join_key_columns: List[str],
        feature_name_columns: List[str],
        timestamp_field: str,
        start_date: datetime.datetime = MIN_DATETIME,
        end_date: datetime.datetime = MAX_DATETIME,
    ) -> pd.DataFrame:
        """Returns the full dataset for training.

        Args:
            join_key_columns: The columns of the join keys.
            feature_name_columns: The columns of the features.
            timestamp_field: The timestamp column.
            start_date: The start of the time range.
            end_date: The end of the time range.

        Returns:
            The historical features as a Pandas DataFrame.
        """
        return RedshiftOfflineStore.pull_all_from_table_or_query(
            config=self.repo_config,
            data_source=self.feature_store.get_data_source(name),
            join_key_columns=join_key_columns,
            feature_name_columns=feature_name_columns,
            timestamp_field=timestamp_field,
            start_date=start_date,
            end_date=end_date,
        ).to_df()

    @property
    def registry(self) -> Registry:
        """Returns the feature store registry.

        Raise:
            ConnectionError: If the online component (Redis) is not available.

        Returns:
            The registry.
        """
        return self.feature_store.registry

    @property
    def feast_version(self) -> str:
        """Returns the version of Feast used.

        Raise:
            ConnectionError: If the online component (Redis) is not available.

        Returns:
            The version of Feast currently being used.
        """
        return str(self.feature_store.version())
