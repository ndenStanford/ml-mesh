"""Feature registration inputs."""

# Standard Library
from typing import List, Optional, Tuple, Callable, Dict

# 3rd party libraries
from pydantic_settings import SettingsConfigDict
from feast import FeatureView

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSettings
from onclusiveml.data.feature_store import FeatureStoreParams, OnDemandFeatureStoreParams
from src.utils import iptc_llm_feature_view_2


class FeatureRegistrationParams(FeatureStoreParams):
    """Feature registration inputs."""

    feast_config_bucket: str
    redshift_database: str
    redshift_table: str = "iptc"
    entity_name: str = "iptc"
    feature_view_name: str = "iptc_feature_view"
    fields: Optional[List[Tuple[str, str]]] = None
    entity_join_key: str = "iptc_id"
    register_features: bool = False

class OnDemandFeatureRegistrationParams(OnDemandFeatureStoreParams):
    feast_config_bucket: str
    config_file: str = "feature_store.yaml"
    local_config_dir: str = "local-config-dir"
    redshift_database: str
    redshift_table: str = "iptc"
    redshift_schema: str = "feast"
    fields: Optional[List[Tuple[str, str]]] = None
    sources: List[str] = ["iptc_feature_view"]
    udf: Callable = iptc_llm_feature_view_2
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


class IptcFirstLevelOnDemandFeatureRegistrationParams(OnclusiveBaseSettings):
    """On-demand feature registration inputs."""

    feature_view_name: str 
    sources: List[str]
    fields: Optional[List[Tuple[str, str]]] = None
    udf: Callable = iptc_llm_feature_view_2
    model_config = SettingsConfigDict(env_prefix="first_level_on_demand_")


class IptcLLMLabelFeatureRegistrationParams(OnclusiveBaseSettings):
    """Feature registration inputs."""

    entity_name: str
    feature_view_name: str
    redshift_table: str
    fields: List[Tuple[str, str]]

    model_config = SettingsConfigDict(env_prefix="llm_label_")



