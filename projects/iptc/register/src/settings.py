"""Feature registration inputs."""

# Standard Library
from typing import Callable, List, Optional, Tuple

# 3rd party libraries
from pydantic_settings import SettingsConfigDict

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSettings
from onclusiveml.data.feature_store import (
    FeatureStoreParams,
    OnDemandFeatureStoreParams,
)

# Source
from src.utils import (
    iptc_first_level_on_demand_feature_view,
    iptc_second_level_on_demand_feature_view,
    iptc_third_level_on_demand_feature_view,
)


class FeatureRegistrationParams(FeatureStoreParams):
    """Feature registration inputs."""

    feast_config_bucket: str
    redshift_database: str
    redshift_table: str = "iptc"
    entity_name: str = "iptc"
    feature_view_name: str = "iptc_feature_view"
    fields: Optional[List[Tuple[str, str]]] = None
    entity_join_key: str = "iptc_id"
    register_features: bool = True


class OnDemandFeatureRegistrationParams(OnDemandFeatureStoreParams):
    """On-demand feature registration inputs."""

    feast_config_bucket: str
    config_file: str = "feature_store.yaml"
    local_config_dir: str = "local-config-dir"
    redshift_database: str
    redshift_table: str = "iptc"
    redshift_schema: str = "feast"
    fields: Optional[List[Tuple[str, str]]] = None
    sources: List[str] = ["iptc_feature_view"]
    udf: Callable = iptc_first_level_on_demand_feature_view
    register_features: bool = True


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


class IptcFirstLevelOnDemandFeatureRegistrationParams(OnclusiveBaseSettings):
    """On-demand feature registration inputs."""

    feature_view_name: str = "iptc_on_demand_feature_view"
    sources: List[str]
    fields: Optional[List[Tuple[str, str]]] = None
    udf: Callable = iptc_first_level_on_demand_feature_view
    model_config = SettingsConfigDict(env_prefix="first_level_on_demand_")


class IptcSecondLevelOnDemandFeatureRegistrationParams(OnclusiveBaseSettings):
    """On-demand feature registration inputs."""

    feature_view_name: str = "iptc_on_demand_feature_view"
    sources: List[str]
    fields: Optional[List[Tuple[str, str]]] = None
    udf: Callable = iptc_second_level_on_demand_feature_view
    model_config = SettingsConfigDict(env_prefix="second_level_on_demand_")


class IptcThirdLevelOnDemandFeatureRegistrationParams(OnclusiveBaseSettings):
    """On-demand feature registration inputs."""

    feature_view_name: str = "iptc_on_demand_feature_view"
    sources: List[str]
    fields: Optional[List[Tuple[str, str]]] = None
    udf: Callable = iptc_third_level_on_demand_feature_view
    model_config = SettingsConfigDict(env_prefix="third_level_on_demand_")


class IptcLLMLabelFeatureRegistrationParams(OnclusiveBaseSettings):
    """Feature registration inputs."""

    entity_name: str
    feature_view_name: str
    redshift_table: str
    fields: List[Tuple[str, str]]

    model_config = SettingsConfigDict(env_prefix="llm_label_")
