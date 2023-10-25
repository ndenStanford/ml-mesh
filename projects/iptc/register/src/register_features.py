"""Register features for IPTC project."""

# 3rd party libraries
from feast import Entity, FeatureView, Field
from feast.types import String

# Internal libraries
from onclusiveml.core.logging import get_default_logger
from onclusiveml.data.feature_store import (
    FeatureStoreHandle,
    RedshiftSourceCustom,
)

# Source
from src.settings import FeatureRegistrationParams  # type: ignore[attr-defined]


logger = get_default_logger(__name__)


def register() -> None:
    """Register features."""
    feature_registration_params = FeatureRegistrationParams()
    logger.info("initializing feature-store handle...")
    fs_handle = FeatureStoreHandle(
        feast_config_bucket=feature_registration_params.feast_config_bucket,
        config_file=feature_registration_params.config_file,
        local_config_dir=feature_registration_params.local_config_dir,
        data_source=feature_registration_params.redshift_table,
    )
    logger.info("Creating datastore...")
    iptc_data_source = RedshiftSourceCustom(
        table=feature_registration_params.redshift_table,
        timestamp_field=feature_registration_params.redshift_timestamp_field,
        database=feature_registration_params.redshift_database,
        schema=feature_registration_params.redshift_schema,
    )

    logger.info("Creating entity...")
    iptc_entity = Entity(
        name=feature_registration_params.entity_name,
        join_keys=[feature_registration_params.entity_join_key],
    )

    logger.info("Creating featureview...")
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

    logger.info("Registering entity...")
    fs_handle.register([iptc_entity])

    logger.info("Registering features...")
    fs_handle.register([iptc_features])

    logger.info(
        f"Registered entities: {[entity.name for entity in fs_handle.list_entities()]}"
    )
    logger.info(
        f"Registered datasources: {[datasource.name for datasource in fs_handle.list_data_sources()]}"
    )
    logger.info(
        f"Registered feature_views: {[feature_view.features for feature_view in fs_handle.list_feature_views()]}"
    )


if __name__ == "__main__":
    register()
