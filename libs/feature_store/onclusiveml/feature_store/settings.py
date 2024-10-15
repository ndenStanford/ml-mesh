"""Feature store settings."""

# 3rd party libraries
from pydantic import SecretStr
from pydantic_settings import SettingsConfigDict

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSettings


class FeatureStoreSettings(OnclusiveBaseSettings):
    """Feature store base settings."""


class FeastFeatureStoreSettings(FeatureStoreSettings):
    """Feast feature store settings."""

    project: str
    mysql_host: str
    mysql_user: str
    mysql_port: str
    mysql_password: SecretStr
    redshift_cluster_id: str
    redshift_cluster_region: str
    redshift_database: str
    redshift_user: str
    redshift_s3_staging_directory: str
    redshift_iam_role: str

    model_config = SettingsConfigDict(
        env_file="config/dev.env",
        extra="forbid",
        env_file_encoding="utf-8",
        validate_assignment=True,
        arbitrary_types_allowed=True,
        env_prefix="onclusiveml_feature_store_",
    )
