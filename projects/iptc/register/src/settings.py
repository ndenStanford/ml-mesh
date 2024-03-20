"""Feature registration inputs."""

# Standard Library
from typing import List, Optional, Tuple

# 3rd party libraries
from pydantic import BaseSettings

# Internal libraries
from onclusiveml.data.feature_store import FeatureStoreParams


class FeatureRegistrationParams(FeatureStoreParams):
    """Feature registration inputs."""

    feast_config_bucket: str
    redshift_database: str
    redshift_table: str = "iptc"
    entity_name: str = "iptc"
    feature_view_name: str = "iptc_feature_view"
    fields: Optional[List[Tuple[str, str]]]
    entity_join_key: str = "iptc_id"
    register_features: bool = False

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class IptcFirstLevelFeatureRegistrationParams(BaseSettings):
    """Feature registration inputs."""

    entity_name: str
    feature_view_name: str
    redshift_table: str
    fields: List[Tuple[str, str]]

    class Config:
        env_prefix = "first_level_"
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class IptcSecondLevelFeatureRegistrationParams(BaseSettings):
    """Feature registration inputs."""

    entity_name: str
    feature_view_name: str
    redshift_table: str
    fields: List[Tuple[str, str]]

    class Config:
        env_prefix = "second_level_"
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class IptcThirdLevelFeatureRegistrationParams(BaseSettings):
    """Feature registration inputs."""

    entity_name: str
    feature_view_name: str
    redshift_table: str
    fields: List[Tuple[str, str]]

    class Config:
        env_prefix = "third_level_"
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"
