"""Settings."""
# Internal libraries
from onclusiveml.tracking import TrackedParams


class IngestionParams(TrackedParams):
    """Ingestion inputs."""

    source_bucket: str
    target_bucket: str
    iptc_level: str
    files: str

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"
