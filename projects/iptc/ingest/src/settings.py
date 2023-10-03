"""Settings."""
# 3rd party libraries
import pyarrow as pa

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


class FirstLevelParquetSchema(TrackedParams):
    """Defines schema for the first level IPTC dataset."""

    schema_dict: dict = {
        "title": pa.string(),
        "score": pa.string(),
        "topic": pa.string(),
        "content": pa.string(),
        "summary": pa.string(),
    }


class FirstLevelMultiLingualTopNParquetSchema(TrackedParams):
    """Defines schema for the first level top N IPTC dataset."""

    schema_dict: dict = {
        "topic_1_0": pa.string(),
        "topic_1_1": pa.string(),
        "topic_1_2": pa.string(),
        "score_0": pa.string(),
        "score_1": pa.string(),
        "score_2": pa.string(),
        "title": pa.string(),
        "content": pa.string(),
        "summary": pa.string(),
        "language": pa.string(),
    }


class FirstLevelMultiLingualParquetSchema(TrackedParams):
    """Defines schema for the first level multi lingual IPTC dataset."""

    schema_dict: dict = {
        "title": pa.string(),
        "score": pa.string(),
        "topic_1": pa.string(),
        "content": pa.string(),
        "summary": pa.string(),
        "language": pa.string(),
    }


class SecondLevelParquetSchema(TrackedParams):
    """Defines schema for the second level IPTC dataset."""

    schema_dict: dict = {
        "topic_1": pa.string(),
        "topic_2": pa.string(),
        "score": pa.string(),
        "title": pa.string(),
        "content": pa.string(),
        "summary": pa.string(),
    }


class SecondLevelMultiLingualParquetSchema(TrackedParams):
    """Defines schema for the second level multi lingual IPTC dataset."""

    schema_dict: dict = {
        "topic_1": pa.string(),
        "topic_2": pa.string(),
        "score": pa.string(),
        "title": pa.string(),
        "content": pa.string(),
        "summary": pa.string(),
        "language": pa.string(),
    }


class ThirdLevelMultiLingualParquetSchema(TrackedParams):
    """Defines schema for the third level multi lingual IPTC dataset."""

    schema_dict: dict = {
        "topic_1": pa.string(),
        "topic_2": pa.string(),
        "topic_3": pa.string(),
        "score": pa.string(),
        "title": pa.string(),
        "content": pa.string(),
        "summary": pa.string(),
        "language": pa.string(),
    }


SCHEMA_MAP = {
    "first_level": FirstLevelParquetSchema(),
    "first_level_multi_lingual": FirstLevelMultiLingualParquetSchema(),
    "first_level_multi_lingual_top_n": FirstLevelMultiLingualTopNParquetSchema(),
    "second_level": SecondLevelParquetSchema(),
    "second_level_multi_lingual": SecondLevelMultiLingualParquetSchema(),
    "third_level_multi_lingual": ThirdLevelMultiLingualParquetSchema(),
}
