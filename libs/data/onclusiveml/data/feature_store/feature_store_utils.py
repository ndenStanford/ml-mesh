"""Utilities for feast feature store."""

# Standard Library
from typing import Any

# 3rd party libraries
from feast import Entity, FeatureView, Field
from feast.types import String
from pydantic import BaseSettings

# Internal libraries
from onclusiveml.data.feature_store import (
    FeatureStoreHandle,
    RedshiftSourceCustom,
)


class FeatureStoreParams(BaseSettings):
    """Base class for all parameter classes in the featurestore module in data library.

    Subclassing from BaseSettings allows for configuring parameters via environment variables.
    """

    feast_config_bucket: str
    config_file: str = "feature_store.yaml"
    local_config_dir: str = "local-config-dir"
    redshift_database: str
    redshift_schema: str = "feast"
    redshift_table: str
    redshift_timestamp_field: str = "event_timestamp"


class FeastRepoBuilder:
    """Utility class Building the components of feast repo."""

    def __init__(self, feature_registration_params: Any) -> None:
        self.feature_registration_params = feature_registration_params
        self.initialize_featurestore_handle()

    def initialize_featurestore_handle(self) -> None:
        """Initializes the FeatureStoreHandle.

        This method sets up the FeatureStoreHandle with the specified parameters
        from the `feature_registration_params` attribute.

        Args:
            None

        Returns:
            None

        """
        self.fs_handle = FeatureStoreHandle(
            feast_config_bucket=self.feature_registration_params.feast_config_bucket,
            config_file=self.feature_registration_params.config_file,
            local_config_dir=self.feature_registration_params.local_config_dir,
            data_source=self.feature_registration_params.redshift_table,
        )

    def build_datasource(self) -> None:
        """Builds a Redshift data source.

        This method creates a RedshiftSourceCustom object and assigns it to
        the `data_source` attribute using the parameters specified in the
        `feature_registration_params` attribute.

        Args:
            None

        Returns:
            None

        """
        self.data_source = RedshiftSourceCustom(
            table=self.feature_registration_params.redshift_table,
            timestamp_field=self.feature_registration_params.redshift_timestamp_field,
            database=self.feature_registration_params.redshift_database,
            schema=self.feature_registration_params.redshift_schema,
        )

    def build_entity(self) -> None:
        """Builds a Feast entity.

        This method creates an Entity object and assigns it to the `entity`
        attribute using the parameters specified in the `feature_registration_params`
        attribute.

        Args:
            None

        Returns:
            None

        """
        self.entity = Entity(
            name=self.feature_registration_params.entity_name,
            join_keys=[self.feature_registration_params.entity_join_key],
        )

    @staticmethod
    def resolve_feast_types(type: str) -> str:
        """Resolves Feast data types.

        This static method maps a string representation of a Feast data type to
        the corresponding Feast data type class.

        Args:
            type (str): String representation of the Feast data type.

        Returns:
            str: The corresponding Feast data type class.

        Raises:
            Exception: If an unknown datatype is passed.

        """
        if type == "String":
            return String
        else:
            raise Exception("Unknown datatype passed!!")

    def build_featureview(self) -> None:
        """Builds a Feast FeatureView.

        This method constructs a FeatureView object and assigns it to the
        `feature_view` attribute using the parameters specified in the
        `feature_registration_params` attribute. It also resolves Feast data types
        using the `resolve_feast_types` method and sets up the feature view's schema.

        Args:
            None

        Returns:
            None

        """
        self.feature_registration_params.fields = [
            (field[0], self.resolve_feast_types(field[1]))
            for field in self.feature_registration_params.fields
        ]
        self.feature_view = FeatureView(
            # The unique name of this feature view. Two feature views in a single
            # project cannot have the same name
            name=self.feature_registration_params.feature_view_name,
            entities=[self.entity],
            # The list of features defined below act as a schema to both define features
            # for both materialization of features into a store, and are used as references
            # during retrieval for building a training dataset or serving features
            schema=[
                Field(name=field[0], dtype=field[1])
                for field in self.feature_registration_params.fields
            ],
            online=False,
            source=self.data_source,
            # Tags are user defined key/value pairs that are attached to each
            # feature view
            tags={},
        )
