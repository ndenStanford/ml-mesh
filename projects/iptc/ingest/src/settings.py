"""Settings."""
# 3rd party libraries
import pyarrow as pa

# Internal libraries
from onclusiveml.core.base.params import Params


class FirstLevelParquetSchema(Params):
    """Defines schema for the first level IPTC dataset."""

    schema_dict: dict = {
        "title": pa.string(),
        "score": pa.string(),
        "topic": pa.string(),
        "content": pa.string(),
        "summary": pa.string(),
    }


class FirstLevelMultiLingualParquetSchema(Params):
    """Defines schema for the first level multi lingual IPTC dataset."""

    schema_dict: dict = {
        "title": pa.string(),
        "score": pa.string(),
        "topic_1": pa.string(),
        "content": pa.string(),
        "summary": pa.string(),
        "language": pa.string(),
    }


class SecondLevelParquetSchema(Params):
    """Defines schema for the second level IPTC dataset."""

    schema_dict: dict = {
        "title": pa.string(),
        "score": pa.string(),
        "topic_1": pa.string(),
        "topic_2": pa.string(),
        "content": pa.string(),
        "summary": pa.string(),
    }


class SecondLevelMultiLingualParquetSchema(Params):
    """Defines schema for the second level multi lingual IPTC dataset."""

    schema_dict: dict = {
        "title": pa.string(),
        "score": pa.float64(),
        "topic_1": pa.string(),
        "topic_2": pa.string(),
        "content": pa.string(),
        "summary": pa.string(),
        "language": pa.string(),
    }


class ThirdLevelParquetSchema(Params):
    """Defines schema for the third level IPTC dataset."""

    schema_dict: dict = {
        "title": pa.string(),
        "score": pa.float64(),
        "topic_1": pa.string(),
        "topic_2": pa.string(),
        "topic_3": pa.string(),
        "content": pa.string(),
        "summary": pa.string(),
    }


class ThirdLevelMultiLingualParquetSchema(Params):
    """Defines schema for the third level multi lingual IPTC dataset."""

    schema_dict: dict = {
        "title": pa.string(),
        "score": pa.float64(),
        "topic_1": pa.string(),
        "topic_2": pa.string(),
        "topic_3": pa.string(),
        "content": pa.string(),
        "summary": pa.string(),
        "language": pa.string(),
    }


SCHEMA_MAP = {
    "first_level": FirstLevelParquetSchema(),
    "first_level_multi_lingual": FirstLevelMultiLingualParquetSchema(),
    "second_level": SecondLevelParquetSchema(),
    "second_level_multi_lingual": SecondLevelMultiLingualParquetSchema(),
    "third_level": ThirdLevelParquetSchema(),
    "third_level_multi_lingual": ThirdLevelMultiLingualParquetSchema(),
}
