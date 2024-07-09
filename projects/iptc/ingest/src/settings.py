"""Settings."""

# Standard Library
from functools import lru_cache

# 3rd party libraries
import pyarrow as pa

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSettings


class IngestionSettings(OnclusiveBaseSettings):
    """Ingestion inputs."""

    source_bucket: str
    target_bucket: str
    iptc_level: str
    data_state: str
    files: str
    shards: int

    @property
    def source_path(self):
        """Source path property."""
        return f"s3://{self.source_bucket}/{self.data_state}/{self.iptc_level}/{self.files}.csv"

    @property
    def target_path(self):
        """Target path property."""
        path = f"s3://{self.target_bucket}/iptc/{self.data_state}/"
        path += f"{self.iptc_level}/{self.files.replace('*','')}"
        return path

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
            + [("iptc_id", pa.int64()), ("event_timestamp", pa.timestamp("ns"))]
        )


class GlobalSettings(IngestionSettings):
    """Global server settings."""


@lru_cache
def get_settings() -> OnclusiveBaseSettings:
    """Returns instanciated global settings class."""
    return GlobalSettings()
