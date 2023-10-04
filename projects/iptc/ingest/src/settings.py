"""Settings."""
# Standard Library
from functools import lru_cache

# 3rd party libraries
from pydantic import BaseSettings


class IngestionSettings(BaseSettings):
    """Ingestion inputs."""

    source_bucket: str
    target_bucket: str
    iptc_level: str
    files: str

    @property
    def source_path(self):
        """Source path property."""
        return f"s3://{self.source_bucket}/raw/{self.iptc_level}/{self.files}.csv"

    @property
    def target_path(self):
        """Target path property."""
        return f"s3://{self.target_bucket}/iptc/{self.iptc_level}/ingested"

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class GlobalSettings(IngestionSettings):
    """Global server settings."""


@lru_cache
def get_settings() -> BaseSettings:
    """Returns instanciated global settings class."""
    return GlobalSettings()
