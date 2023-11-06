"""Feature registration inputs."""
# Internal libraries
from onclusiveml.data.feature_store import FeatureStoreParams


class FeatureRegistrationParams(FeatureStoreParams):
    """Feature registration inputs."""

    feast_config_bucket: str
    config_file: str
    local_config_dir: str
    entity_name: str
    entity_join_key: str
    feature_view_name: str
    redshift_database: str
    redshift_schema: str
    redshift_table: str
    redshift_timestamp_field: str

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"
