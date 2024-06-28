"""Feature registration inputs."""

# Standard Library
from typing import List, Optional, Tuple

# 3rd party libraries
from pydantic_settings import SettingsConfigDict

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSettings
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


class IptcFirstLevelFeatureRegistrationParams(OnclusiveBaseSettings):
    """Feature registration inputs."""

    entity_name: str
    feature_view_name: str
    redshift_table: str
    fields: List[Tuple[str, str]]

    model_config = SettingsConfigDict(env_prefix="first_level_")


class IptcSecondLevelFeatureRegistrationParams(OnclusiveBaseSettings):
    """Feature registration inputs."""

    entity_name: str
    feature_view_name: str
    redshift_table: str
    fields: List[Tuple[str, str]]

    model_config = SettingsConfigDict(env_prefix="second_level_")


class IptcThirdLevelFeatureRegistrationParams(OnclusiveBaseSettings):
    """Feature registration inputs."""

    entity_name: str
    feature_view_name: str
    redshift_table: str
    fields: List[Tuple[str, str]]

    model_config = SettingsConfigDict(env_prefix="third_level_")
