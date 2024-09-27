"""Feature registration inputs."""

# Standard Library
from typing import List, Optional, Tuple

# 3rd party libraries
from pydantic_settings import SettingsConfigDict

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSettings
from onclusiveml.feature_store import FeatureStoreParams


class FeatureRegistrationParams(FeatureStoreParams):
    """Feature registration inputs."""

    feast_config_bucket: str
    redshift_database: str
    redshift_table: str = "visitor-estimation"
    entity_name: str = "visitor-estimation"
    feature_view_name: str = "visitor_estimation_feature_view"
    fields: Optional[List[Tuple[str, str]]] = None
    entity_join_key: str = "visitor_estimation_id"
    register_features: bool = False
    timestamp_field: str = "event_timestamp"


class CrawlerItemsFeatureRegistrationParams(OnclusiveBaseSettings):
    """Feature registration inputs for CRAWLER_ITEMS."""

    entity_name: str
    feature_view_name: str
    redshift_table: str
    fields: List[Tuple[str, str]]
    join_key: str

    model_config = SettingsConfigDict(env_prefix="crawler_items_")


class EclrLinksFeatureRegistrationParams(OnclusiveBaseSettings):
    """Feature registration inputs for ECLR_LINKS."""

    entity_name: str
    feature_view_name: str
    redshift_table: str
    fields: List[Tuple[str, str]]
    join_key: str

    model_config = SettingsConfigDict(env_prefix="eclr_links_")


class EntityConnectionsFeatureRegistrationParams(OnclusiveBaseSettings):
    """Feature registration inputs for ENTITY_CONNECTIONS."""

    entity_name: str
    feature_view_name: str
    redshift_table: str
    fields: List[Tuple[str, str]]
    join_key: str

    model_config = SettingsConfigDict(env_prefix="entity_connections_")


class EntityEaPerFeatureRegistrationParams(OnclusiveBaseSettings):
    """Feature registration inputs for ENTITY_EA_PR."""

    entity_name: str
    feature_view_name: str
    redshift_table: str
    fields: List[Tuple[str, str]]
    join_key: str

    model_config = SettingsConfigDict(env_prefix="entity_ea_per_")


class EntityLinksLmdFeatureRegistrationParams(OnclusiveBaseSettings):
    """Feature registration inputs for ENTITY_LINKS_LMD."""

    entity_name: str
    feature_view_name: str
    redshift_table: str
    fields: List[Tuple[str, str]]
    join_key: str

    model_config = SettingsConfigDict(env_prefix="entity_links_lmd_")


class EntityLinksFeatureRegistrationParams(OnclusiveBaseSettings):
    """Feature registration inputs for ENTITY_LINKS."""

    entity_name: str
    feature_view_name: str
    redshift_table: str
    fields: List[Tuple[str, str]]
    join_key: str

    model_config = SettingsConfigDict(env_prefix="entity_links_")


class ProfileCompanySectorsFeatureRegistrationParams(OnclusiveBaseSettings):
    """Feature registration inputs for PROFILE_COMPANY_SECTORS."""

    entity_name: str
    feature_view_name: str
    redshift_table: str
    fields: List[Tuple[str, str]]
    join_key: str

    model_config = SettingsConfigDict(env_prefix="profile_company_sectors_")


class SearchSeedsFeatureRegistrationParams(OnclusiveBaseSettings):
    """Feature registration inputs for SEARCH_SEEDS."""

    entity_name: str
    feature_view_name: str
    redshift_table: str
    fields: List[Tuple[str, str]]
    join_key: str

    model_config = SettingsConfigDict(env_prefix="search_seeds_")


class DomainsFeatureRegistrationParams(OnclusiveBaseSettings):
    """Feature registration inputs for DOMAINS."""

    entity_name: str
    feature_view_name: str
    redshift_table: str
    fields: List[Tuple[str, str]]
    join_key: str

    model_config = SettingsConfigDict(env_prefix="domains_")


class ProfileEntityRelationshipsFeatureRegistrationParams(OnclusiveBaseSettings):
    """Feature registration inputs for PROFILE_ENTITY_RELATIONSHIPS."""

    entity_name: str
    feature_view_name: str
    redshift_table: str
    fields: List[Tuple[str, str]]
    join_key: str

    model_config = SettingsConfigDict(env_prefix="profile_entity_relationships_")
