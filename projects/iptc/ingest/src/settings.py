"""Settings."""
# 3rd party libraries
import pyarrow as pa

# Internal libraries
from onclusiveml.core.base.params import Params


class FirstLevelParquetSchema(Params):
    """Defines schema for the first level IPTC dataset."""

    schema_dict: dict = {
        "title": pa.large_string(),
        "score": pa.large_string(),
        "topic": pa.large_string(),
        "content": pa.large_string(),
        "summary": pa.large_string(),
    }


class FirstLevelMultiLingualTopNParquetSchema(Params):
    """Defines schema for the first level top N IPTC dataset."""

    schema_dict: dict = {
        "topic_1_0": pa.large_string(),
        "topic_1_1": pa.large_string(),
        "topic_1_2": pa.large_string(),
        "score_0": pa.large_string(),
        "score_1": pa.large_string(),
        "score_2": pa.large_string(),
        "title": pa.large_string(),
        "content": pa.large_string(),
        "summary": pa.large_string(),
        "language": pa.large_string(),
    }


class FirstLevelMultiLingualParquetSchema(Params):
    """Defines schema for the first level multi lingual IPTC dataset."""

    schema_dict: dict = {
        "title": pa.large_string(),
        "score": pa.large_string(),
        "topic_1": pa.large_string(),
        "content": pa.large_string(),
        "summary": pa.large_string(),
        "language": pa.large_string(),
    }


class SecondLevelParquetSchema(Params):
    """Defines schema for the second level IPTC dataset."""

    schema_dict: dict = {
        "topic_1": pa.large_string(),
        "topic_2": pa.large_string(),
        "score": pa.large_string(),
        "title": pa.large_string(),
        "content": pa.large_string(),
        "summary": pa.large_string(),
    }


class SecondLevelMultiLingualParquetSchema(Params):
    """Defines schema for the second level multi lingual IPTC dataset."""

    schema_dict: dict = {
        "topic_1": pa.large_string(),
        "topic_2": pa.large_string(),
        "score": pa.large_string(),
        "title": pa.large_string(),
        "content": pa.large_string(),
        "summary": pa.large_string(),
        "language": pa.large_string(),
    }


class ThirdLevelMultiLingualParquetSchema(Params):
    """Defines schema for the third level multi lingual IPTC dataset."""

    schema_dict: dict = {
        "topic_1": pa.large_string(),
        "topic_2": pa.large_string(),
        "topic_3": pa.large_string(),
        "score": pa.large_string(),
        "title": pa.large_string(),
        "content": pa.large_string(),
        "summary": pa.large_string(),
        "language": pa.large_string(),
    }


SCHEMA_MAP = {
    "first_level": FirstLevelParquetSchema(),
    "first_level_multi_lingual": FirstLevelMultiLingualParquetSchema(),
    "first_level_multi_lingual_top_n": FirstLevelMultiLingualTopNParquetSchema(),
    "second_level": SecondLevelParquetSchema(),
    "second_level_multi_lingual": SecondLevelMultiLingualParquetSchema(),
    "third_level_multi_lingual": ThirdLevelMultiLingualParquetSchema(),
}
