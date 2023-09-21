"""Settings."""

# Internal libraries
from onclusiveml.core.base.params import Params


class FirstLevelSchema(Params):
    """Defines schema for the first level IPTC dataset."""

    dir_name: str = "first_level"
    schema_dict: dict = {
        "title": str,
        "score": float,
        "topic": str,
        "content": str,
        "summary": str,
    }


class FirstLevelMultiLingualSchema(Params):
    """Defines schema for the first level multi lingual IPTC dataset."""

    dir_name: str = "first_level_multi_lingual"
    schema_dict: dict = {
        "title": str,
        "score": float,
        "topic": str,
        "content": str,
        "summary": str,
        "language": str,
    }


class SecondLevelSchema(Params):
    """Defines schema for the second level IPTC dataset."""

    dir_name: str = "second_level"
    schema_dict: dict = {
        "title": str,
        "score": float,
        "topic_1": str,
        "topic_2": str,
        "content": str,
        "summary": str,
    }


class SecondLevelMultiLingualSchema(Params):
    """Defines schema for the second level multi lingual IPTC dataset."""

    dir_name: str = "second_level_multi_lingual"
    schema_dict: dict = {
        "title": str,
        "score": float,
        "topic_1": str,
        "topic_2": str,
        "content": str,
        "summary": str,
        "language": str,
    }


class ThirdLevelSchema(Params):
    """Defines schema for the third level IPTC dataset."""

    dir_name: str = "third_level"
    schema_dict: dict = {
        "title": str,
        "score": float,
        "topic_1": str,
        "topic_2": str,
        "topic_3": str,
        "content": str,
        "summary": str,
    }


class ThirdLevelMultiLingualSchema(Params):
    """Defines schema for the third level multi lingual IPTC dataset."""

    dir_name: str = "third_level_multi_lingual"
    schema_dict: dict = {
        "title": str,
        "score": float,
        "topic_1": str,
        "topic_2": str,
        "topic_3": str,
        "content": str,
        "summary": str,
        "language": str,
    }


SCHEMA_MAP = {
    "first_level": FirstLevelSchema(),
    "first_level_multi_lingual": FirstLevelMultiLingualSchema(),
    "second_level": SecondLevelSchema(),
    "second_level_multi_lingual": SecondLevelMultiLingualSchema(),
    "third_level": ThirdLevelSchema(),
    "third_level_multi_lingual": ThirdLevelMultiLingualSchema(),
}
