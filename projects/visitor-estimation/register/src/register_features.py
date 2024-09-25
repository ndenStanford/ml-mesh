"""Register features for VISITOR ESTIMATION project."""

# Standard Library
from typing import Any

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSettings
from onclusiveml.core.logging import get_default_logger
from onclusiveml.core.logging.constants import OnclusiveService
from onclusiveml.feature_store import FeastRepoBuilder, FeatureStoreParams

# Source
from src.settings import (  # type: ignore[attr-defined]
    CrawlerItemsFeatureRegistrationParams,
    DomainsFeatureRegistrationParams,
    EclrLinksFeatureRegistrationParams,
    EntityConnectionsFeatureRegistrationParams,
    EntityEaPerFeatureRegistrationParams,
    EntityLinksFeatureRegistrationParams,
    EntityLinksLmdFeatureRegistrationParams,
    FeatureRegistrationParams,
    ProfileCompanySectorsFeatureRegistrationParams,
    ProfileEntityRelationshipsFeatureRegistrationParams,
    SearchSeedsFeatureRegistrationParams,
)


logger = get_default_logger(
    name=__name__, service=OnclusiveService.VISITOR_ESTIMATION.value
)


def main() -> None:
    """Register features."""
    feature_registration_params = FeatureRegistrationParams()
    # Instantiate each feature registration class
    crawler_items_feature_registration_params = CrawlerItemsFeatureRegistrationParams()
    entity_connections_feature_registration_params = (
        EntityConnectionsFeatureRegistrationParams()
    )
    entity_ea_pr_feature_registration_params = EntityEaPerFeatureRegistrationParams()
    entity_links_lmd_feature_registration_params = (
        EntityLinksLmdFeatureRegistrationParams()
    )
    entity_links_feature_registration_params = EntityLinksFeatureRegistrationParams()
    profile_company_sectors_feature_registration_params = (
        ProfileCompanySectorsFeatureRegistrationParams()
    )
    search_seeds_feature_registration_params = SearchSeedsFeatureRegistrationParams()
    domains_feature_registration_params = DomainsFeatureRegistrationParams()
    profile_entity_relationships_feature_registration_params = (
        ProfileEntityRelationshipsFeatureRegistrationParams()
    )
    eclr_links_feature_registration_params = EclrLinksFeatureRegistrationParams()
    # Register each feature
    register(feature_registration_params, crawler_items_feature_registration_params)
    register(
        feature_registration_params, entity_connections_feature_registration_params
    )
    register(feature_registration_params, entity_ea_pr_feature_registration_params)
    register(feature_registration_params, entity_links_lmd_feature_registration_params)
    register(feature_registration_params, entity_links_feature_registration_params)
    register(
        feature_registration_params, profile_company_sectors_feature_registration_params
    )
    register(feature_registration_params, search_seeds_feature_registration_params)
    register(feature_registration_params, domains_feature_registration_params)
    register(
        feature_registration_params,
        profile_entity_relationships_feature_registration_params,
    )
    register(feature_registration_params, eclr_links_feature_registration_params)

    logger.info("Feature registration completed successfully.")


def register(
    feature_registration_params: FeatureStoreParams,
    ve_feature_registration_params: OnclusiveBaseSettings,
) -> None:
    """Register features."""
    print(ve_feature_registration_params.entity_name)
    feature_registration_params.entity_name = ve_feature_registration_params.entity_name
    feature_registration_params.feature_view_name = (
        ve_feature_registration_params.feature_view_name
    )
    feature_registration_params.redshift_table = (
        ve_feature_registration_params.redshift_table
    )
    feature_registration_params.fields = ve_feature_registration_params.fields

    feature_registration_params.entity_join_key = (
        ve_feature_registration_params.join_key
    )

    logger.info("Creating feast-repo builder...")
    feast_repo_builder = FeastRepoBuilder(feature_registration_params)

    logger.info("Creating datastore...")
    feast_repo_builder.build_datasource()

    logger.info("Creating entity...")
    feast_repo_builder.build_entity()

    logger.info("Creating featureview...")
    feast_repo_builder.build_featureview()
    register_repo_contents(
        feast_repo_builder
    )  # TODO: add plan and conditional registeration


def register_repo_contents(feast_repo_builder: Any) -> None:
    """Registers entity, features, and logs registration information.

    This function uses the Feast FeatureStoreHandle to register the Feast entity and
    feature view created by the FeastRepoBuilder. It also logs information about the
    registered entities, data sources, and feature views.

    Args:
        feast_repo_builder (Any): FeastRepoBuilder object containing entity and
            feature view.

    Returns:
        None

    """
    logger.info("Registering entity...")
    feast_repo_builder.fs_handle.register([feast_repo_builder.entity])
    logger.info("Registering features...")
    feast_repo_builder.fs_handle.register([feast_repo_builder.feature_view])
    logger.info(
        f"Registered entities: "
        f"{[entity.name for entity in feast_repo_builder.fs_handle.list_entities()]}"
    )
    logger.info(
        f"Registered datasources: "
        f"{[datasource.name for datasource in feast_repo_builder.fs_handle.list_data_sources()]}"
    )
    feature_views_list = feast_repo_builder.fs_handle.list_feature_views()
    logger.info(
        f"Registered feature views: "
        f"{[(fv.projection.name, fv.features) for fv in feature_views_list]}"
    )


def plan_repo_contents(feast_repo_builder: Any) -> None:
    """Generates a plan for registering feast components and logs the differences.

    This function uses the Feast FeatureStoreHandle to generate a plan for registering
    the specified data source, feature view, and entity. It then logs the registry
    difference, infrastructure difference, and new infrastructure.

    Args:
        feast_repo_builder (Any): FeastRepoBuilder object containing data source,
            feature view, entity, and FeatureStoreHandle.

    Returns:
        None

    """
    registry_diff, infra_diff, new_infra = feast_repo_builder.fs_handle.plan(
        [feast_repo_builder.data_source],
        [feast_repo_builder.feature_view],
        [feast_repo_builder.entity],
    )
    logger.info(f"Registry diff : {registry_diff.to_string()}")
    logger.info(f"Infra diff : {infra_diff}")
    logger.info(f"New Infra : {new_infra}")


if __name__ == "__main__":
    main()
