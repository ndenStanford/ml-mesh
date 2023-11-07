"""Feature registration inputs."""
# Internal libraries
from onclusiveml.data.feature_store import FeatureStoreParams


class FeatureRegistrationParams(FeatureStoreParams):
    """Feature registration inputs."""

    feast_config_bucket: str = "kubeflow-feast-config-dev"
    config_file: str = "feature_store.yaml"
    local_config_dir: str = "local-config-dir"
    entity_name: str = "topic"
    entity_join_key: str = "iptc_id"
    feature_view_name: str = "topic_feature_view"
    redshift_database: str = "sources_dev"
    redshift_schema: str = "feast"
    redshift_table: str = "topic"
    redshift_timestamp_field: str = "event_timestamp"

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"
