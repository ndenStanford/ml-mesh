"""Settings."""

# Standard Library
import os
from typing import List

# 3rd party libraries
from pydantic_settings import SettingsConfigDict

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSettings
from onclusiveml.feature_store import FeatureStoreParams
from onclusiveml.tracking import (
    TrackedModelCard,
    TrackedModelSettings,
    TrackingSettings,
)


class DataFetchParams(FeatureStoreParams):
    """Feature registration inputs."""

    dataset_upload_bucket: str
    dataset_upload_dir: str
    entity_name: str = "visitor-estimation"
    entity_join_key: str = "visitor_estimation_id"
    redshift_table: str = "stg_visitor_estimation"
    feature_view_name: str = "visitor_estimation_feature_view"
    redshift_timestamp_field: str
    save_artifact: bool = False
    n_records_sample: int
    n_records_full: int
    filter_columns: List[str] = []
    filter_values: List[str] = []
    comparison_operators: List[str] = []
    non_nullable_columns: List[str] = []


class CrawlerItemsDataFetchParams(OnclusiveBaseSettings):
    """Feature registration inputs."""

    entity_name: str
    entity_join_key: str
    redshift_table: str
    feature_view_name: str

    model_config = SettingsConfigDict(env_prefix="crawler_items_")


class EclrLinksDataFetchParams(OnclusiveBaseSettings):
    """Data fetch parameters for ECLR_LINKS."""

    entity_name: str
    entity_join_key: str
    redshift_table: str
    feature_view_name: str

    model_config = SettingsConfigDict(env_prefix="eclr_links_")


class EntityConnectionsDataFetchParams(OnclusiveBaseSettings):
    """Data fetch parameters for ENTITY_CONNECTIONS."""

    entity_name: str
    entity_join_key: str
    redshift_table: str
    feature_view_name: str

    model_config = SettingsConfigDict(env_prefix="entity_connections_")


class EntityEaPerDataFetchParams(OnclusiveBaseSettings):
    """Data fetch parameters for ENTITY_EA_PR."""

    entity_name: str
    entity_join_key: str
    redshift_table: str
    feature_view_name: str

    model_config = SettingsConfigDict(env_prefix="entity_ea_per_")


class EntityLinksLmdDataFetchParams(OnclusiveBaseSettings):
    """Data fetch parameters for ENTITY_LINKS_LMD."""

    entity_name: str
    entity_join_key: str
    redshift_table: str
    feature_view_name: str

    model_config = SettingsConfigDict(env_prefix="entity_links_lmd_")


class EntityLinksDataFetchParams(OnclusiveBaseSettings):
    """Data fetch parameters for ENTITY_LINKS."""

    entity_name: str
    entity_join_key: str
    redshift_table: str
    feature_view_name: str

    model_config = SettingsConfigDict(env_prefix="entity_links_")


class ProfileCompanySectorsDataFetchParams(OnclusiveBaseSettings):
    """Data fetch parameters for PROFILE_COMPANY_SECTORS."""

    entity_name: str
    entity_join_key: str
    redshift_table: str
    feature_view_name: str

    model_config = SettingsConfigDict(env_prefix="profile_company_sectors_")


class SearchSeedsDataFetchParams(OnclusiveBaseSettings):
    """Data fetch parameters for SEARCH_SEEDS."""

    entity_name: str
    entity_join_key: str
    redshift_table: str
    feature_view_name: str

    model_config = SettingsConfigDict(env_prefix="search_seeds_")


class DomainsDataFetchParams(OnclusiveBaseSettings):
    """Data fetch parameters for DOMAINS."""

    entity_name: str
    entity_join_key: str
    redshift_table: str
    feature_view_name: str

    model_config = SettingsConfigDict(env_prefix="domains_")


class ProfileEntityRelationshipsDataFetchParams(OnclusiveBaseSettings):
    """Data fetch parameters for PROFILE_ENTITY_RELATIONSHIPS."""

    entity_name: str
    entity_join_key: str
    redshift_table: str
    feature_view_name: str

    model_config = SettingsConfigDict(env_prefix="profile_entity_relationships_")


class TrackedVEModelSpecs(TrackedModelSettings):
    """Tracked iptc model settings."""

    project: str = "onclusive/visitor-estimation"
    model: str = "VE-TRAINED"


class VEModelParams(TrackingSettings):
    """the training argument for visitor estimation training."""

    max_depth: int = 10
    n_estimators: int = 20
    min_window: int = 30
    max_window: int = 30
    excluded_profiles: str = "2,12,20,28"
    included_profiles: str = ""
    index_features: list = ["type", "category_id", "company_sector_id"]
    encode_features: list = ["type", "category_id"]
    exclude_features: list = []
    interact: list = []
    min_entity_date: str = "2012-01-01"
    remove_zero_visitor: bool = False


class TrackedVEBaseModelCard(TrackedModelCard):
    """The model card for the base model of the iptc ML project."""

    model_type: str = "trained"
    # --- custom fields
    # model params
    model_params: VEModelParams = VEModelParams()
    # admin
    local_output_dir: str = os.path.join(".", "ve_model_artifacts")
    logging_level: str = "INFO"
