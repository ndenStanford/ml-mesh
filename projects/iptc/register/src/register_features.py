"""Register features for IPTC project."""

# 3rd party libraries
import feast
from feast import Entity, FeatureView, Field
from feast.types import String
from src.settings import FeatureRegistrationParams

# Internal libraries
from onclusiveml.data.feature_store import (
    FeatureStoreHandle,
    RedshiftSourceCustom,
)


def register() -> None:
    """Register features."""
    feature_registration_params = FeatureRegistrationParams()
    fs_handle = FeatureStoreHandle(
        feast_config_bucket=feature_registration_params.feast_config_bucket,
        config_file=feature_registration_params.config_file,
        local_config_dir=feature_registration_params.local_config_dir,
    )

    iptc_data_source = RedshiftSourceCustom(
        table=feature_registration_params.redshift_table,
        timestamp_field=feature_registration_params.redshift_timestamp_field,
        database=feature_registration_params.redshift_database,
        schema=feature_registration_params.redshift_schema,
    )

    iptc_entity = Entity(
        name=feature_registration_params.entity_name,
        join_keys=[feature_registration_params.entity_join_key],
    )

    iptc_features = FeatureView(
        # The unique name of this feature view. Two feature views in a single
        # project cannot have the same name
        name=feature_registration_params.feature_view_name,
        entities=[iptc_entity],
        # The list of features defined below act as a schema to both define features
        # for both materialization of features into a store, and are used as references
        # during retrieval for building a training dataset or serving features
        schema=[
            Field(name="topic_1", dtype=String),
            Field(name="topic_2", dtype=String),
            Field(name="title", dtype=String),
            Field(name="language", dtype=String),
            Field(name="content", dtype=String),
        ],
        online=False,
        source=iptc_data_source,
        # Tags are user defined key/value pairs that are attached to each
        # feature view
        tags={},
    )

    fs_handle.register([iptc_entity])
    fs_handle.register([iptc_features])


if __name__ == "__main__":
    register()
