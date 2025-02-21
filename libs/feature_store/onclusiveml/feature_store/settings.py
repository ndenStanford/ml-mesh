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

    project: str = "project"
    mysql_host: str = "mysql_host"
    mysql_user: str = "mysql_user"
    mysql_port: str = "mysql_port"
    mysql_password: SecretStr = "mysql_password"
    redshift_cluster_id: str = "redshift_cluster_id"
    redshift_cluster_region: str = "redshift_cluster_region"
    redshift_database: str = "redshift_database"
    redshift_user: str = "redshift_user"
    redshift_s3_staging_directory: str = "redshift_s3_staging_directory"
    redshift_iam_role: str = "redshift_iam_role"

    model_config = SettingsConfigDict(
        extra="forbid",
        env_file_encoding="utf-8",
        validate_assignment=True,
        arbitrary_types_allowed=True,
        env_prefix="onclusiveml_feature_store_",
    )
