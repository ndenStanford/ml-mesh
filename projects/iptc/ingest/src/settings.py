"""Settings."""
# 3rd party libraries
import pyarrow as pa

# Internal libraries
from onclusiveml.core.base.params import Params


class FirstLevelSchema(Params):
    """Defines schema for the first level IPTC dataset."""

    dir_name: str = "first_level"
    schema_dict: dict = {
        "title": pa.string(),
        "score": pa.float64(),
        "topic": pa.string(),
        "content": pa.string(),
        "summary": pa.string(),
    }


class FirstLevelMultiLingualSchema(Params):
    """Defines schema for the first level multi lingual IPTC dataset."""

    dir_name: str = "first_level_multi_lingual"
    schema_dict: dict = {
        "title": pa.string(),
        "score": pa.float64(),
        "topic": pa.string(),
        "content": pa.string(),
        "summary": pa.string(),
        "language": pa.string(),
    }


class SecondLevelSchema(Params):
    """Defines schema for the second level IPTC dataset."""

    dir_name: str = "second_level"
    schema_dict: dict = {
        "title": pa.string(),
        "score": pa.float64(),
        "topic_1": pa.string(),
        "topic_2": pa.string(),
        "content": pa.string(),
        "summary": pa.string(),
    }


class SecondLevelMultiLingualSchema(Params):
    """Defines schema for the second level multi lingual IPTC dataset."""

    dir_name: str = "second_level_multi_lingual"
    schema_dict: dict = {
        "title": pa.string(),
        "score": pa.float64(),
        "topic_1": pa.string(),
        "topic_2": pa.string(),
        "content": pa.string(),
        "summary": pa.string(),
        "language": pa.string(),
    }


class ThirdLevelSchema(Params):
    """Defines schema for the third level IPTC dataset."""

    dir_name: str = "third_level"
    schema_dict: dict = {
        "title": pa.string(),
        "score": pa.float64(),
        "topic_1": pa.string(),
        "topic_2": pa.string(),
        "topic_3": pa.string(),
        "content": pa.string(),
        "summary": pa.string(),
    }


class ThirdLevelMultiLingualSchema(Params):
    """Defines schema for the third level multi lingual IPTC dataset."""

    dir_name: str = "third_level_multi_lingual"
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
    "first_level": FirstLevelSchema(),
    "first_level_multi_lingual": FirstLevelMultiLingualSchema(),
    "second_level": SecondLevelSchema(),
    "second_level_multi_lingual": SecondLevelMultiLingualSchema(),
    "third_level": ThirdLevelSchema(),
    "third_level_multi_lingual": ThirdLevelMultiLingualSchema(),
}
