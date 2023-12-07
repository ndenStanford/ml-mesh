"""Settings."""
# Standard Library
from functools import lru_cache

# 3rd party libraries
import pyarrow as pa
from pydantic import BaseSettings


class IngestionSettings(BaseSettings):
    """Ingestion inputs."""

    source_bucket: str
    target_bucket: str
    iptc_level: str
    files: str
    shards: int

    @property
    def source_path(self):
        """Source path property."""
        return f"s3://{self.source_bucket}/raw/{self.iptc_level}/{self.files}.csv"

    @property
    def target_path(self):
        """Target path property."""
        return f"s3://{self.target_bucket}/iptc/{self.iptc_level}/{self.files.replace('*','')}"

    @property
    def schema(self):
        """Schema property."""
        map = {
            "first_level": [
                "topic_1",
                "title",
                "content",
            ],
            "first_level_multi_lingual": [
                "topic_1",
                "title",
                "content",
                "language",
            ],
            "first_level_multi_lingual_top_n": [
                "topic_1_0",
                "topic_1_1",
                "topic_1_2",
                "title",
                "content",
                "language",
            ],
            "second_level_multi_lingual": [
                "topic_1",
                "topic_2",
                "title",
                "content",
                "language",
            ],
            "second_level": [
                "topic_1",
                "topic_2",
                "title",
                "content",
            ],
            "third_level_multi_lingual": [
                "topic_1",
                "topic_2",
                "topic_3",
                "title",
                "content",
                "summary",
                "language",
            ],
        }
        return map[self.iptc_level]

    @property
    def output_schema(self):
        """Ouput schema property."""
        return pa.schema(
            [(k, pa.string()) for k in self.schema]
            + [("id", pa.int64()), ("timestamp", pa.timestamp("ns"))]
        )

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class GlobalSettings(IngestionSettings):
    """Global server settings."""


@lru_cache
def get_settings() -> BaseSettings:
    """Returns instanciated global settings class."""
    return GlobalSettings()
