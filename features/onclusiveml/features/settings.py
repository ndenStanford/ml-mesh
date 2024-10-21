"""Settings."""

from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import (
    SettingsConfigDict,
)
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists
from onclusiveml.core import OnclusiveBaseSettings


class GlobalSettings(OnclusiveBaseSettings):
    """Feature store global settings."""

    project: str = "feature_store_dev"
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
        extra="forbid",
        env_file_encoding="utf-8",
        validate_assignment=True,
        arbitrary_types_allowed=True,
        env_prefix="onclusiveml_feature_store_",
    )

    @property
    def mysql_registry_path(self) -> str:
        """Mysql registry path."""
        url = f"mysql+pymysql://{self.mysql_user}:{self.mysql_password.get_secret_value()}@{self.mysql_host}:{self.mysql_port}/feast"  # noqa: E501
        engine = create_engine(url)
        if not database_exists(engine.url):
            create_database(engine.url)
        return url


@lru_cache
def get_settings() -> OnclusiveBaseSettings:
    """Returns instanciated global settings class."""
    return GlobalSettings()
