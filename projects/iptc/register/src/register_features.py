"""Register features for IPTC project."""

# Standard Library
from typing import Any

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSettings
from onclusiveml.core.logging import get_default_logger
from onclusiveml.core.logging.constants import OnclusiveService
from onclusiveml.feature_store import FeastRepoBuilder, FeatureStoreParams

# Source
from src.settings import (  # type: ignore[attr-defined]; FeatureRegistrationLLMParams,
    FeatureRegistrationParams,
    IptcFirstLevelFeatureRegistrationParams,
    IptcFirstLevelOnDemandFeatureRegistrationParams,
    IptcFourthLevelOnDemandFeatureRegistrationParams,
    IptcSecondLevelFeatureRegistrationParams,
    IptcSecondLevelOnDemandFeatureRegistrationParams,
    IptcThirdLevelFeatureRegistrationParams,
    IptcThirdLevelOnDemandFeatureRegistrationParams,
    OnDemandFeatureRegistrationParams,
)


logger = get_default_logger(name=__name__, service=OnclusiveService.IPTC_REGISTER.value)


def main() -> None:
    """Register features."""
    feature_registration_params = FeatureRegistrationParams()
    iptc_first_level_feature_registration_params = (
        IptcFirstLevelFeatureRegistrationParams()
    )
    register(feature_registration_params, iptc_first_level_feature_registration_params)
    iptc_second_level_feature_registration_params = (
        IptcSecondLevelFeatureRegistrationParams()
    )
    register(feature_registration_params, iptc_second_level_feature_registration_params)
    iptc_third_level_feature_registration_params = (
        IptcThirdLevelFeatureRegistrationParams()
    )
    register(feature_registration_params, iptc_third_level_feature_registration_params)
    on_demand_feature_registration_params = OnDemandFeatureRegistrationParams()
    iptc_first_level_on_demand_feature_registration_params = (
        IptcFirstLevelOnDemandFeatureRegistrationParams()
    )
    register_on_demand(
        on_demand_feature_registration_params,
        iptc_first_level_on_demand_feature_registration_params,
    )
    iptc_second_level_on_demand_feature_registration_params = (
        IptcSecondLevelOnDemandFeatureRegistrationParams()
    )
    register_on_demand(
        on_demand_feature_registration_params,
        iptc_second_level_on_demand_feature_registration_params,
    )
    iptc_third_level_on_demand_feature_registration_params = (
        IptcThirdLevelOnDemandFeatureRegistrationParams()
    )
    register_on_demand(
        on_demand_feature_registration_params,
        iptc_third_level_on_demand_feature_registration_params,
    )
    iptc_fourth_level_on_demand_feature_registration_params = (
        IptcFourthLevelOnDemandFeatureRegistrationParams()
    )
    register_on_demand(
        on_demand_feature_registration_params,
        iptc_fourth_level_on_demand_feature_registration_params,
    )


def register(
    feature_registration_params: FeatureStoreParams,
    iptc_level_feature_registration_params: OnclusiveBaseSettings,
) -> None:
    """Register features."""
    feature_registration_params.entity_name = (
        iptc_level_feature_registration_params.entity_name
    )
    feature_registration_params.feature_view_name = (
        iptc_level_feature_registration_params.feature_view_name
    )
    feature_registration_params.redshift_table = (
        iptc_level_feature_registration_params.redshift_table
    )
    feature_registration_params.fields = iptc_level_feature_registration_params.fields

    logger.info("Creating feast-repo builder...")
    feast_repo_builder = FeastRepoBuilder(feature_registration_params)

    logger.info("Creating datastore...")
    feast_repo_builder.build_datasource()

    logger.info("Creating entity...")
    feast_repo_builder.build_entity()

    logger.info("Creating featureview...")
    feast_repo_builder.build_featureview()
    # plan_repo_contents(feast_repo_builder)
    if feature_registration_params.register_features:
        register_repo_contents(feast_repo_builder)


def register_on_demand(
    feature_registration_params: OnDemandFeatureRegistrationParams,
    iptc_level_on_demand_feature_registration_params: OnclusiveBaseSettings,
) -> None:
    """Register features."""
    feature_registration_params.sources = (
        iptc_level_on_demand_feature_registration_params.sources
    )
    feature_registration_params.fields = (
        iptc_level_on_demand_feature_registration_params.fields
    )
    feature_registration_params.udf = (
        iptc_level_on_demand_feature_registration_params.udf
    )

    logger.info("Creating feast-repo builder...")
    feast_repo_builder = FeastRepoBuilder(feature_registration_params)

    logger.info("Creating on-demand featureview...")
    feast_repo_builder.build_on_demand_featureview()

    if feature_registration_params.register_features:
        register_on_demand_repo_contents(feast_repo_builder)


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


def register_on_demand_repo_contents(feast_repo_builder: Any) -> None:
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
    logger.info("Registering features...")
    feast_repo_builder.fs_handle.register([feast_repo_builder.feature_view])
    feature_views_list = feast_repo_builder.fs_handle.list_on_demand_feature_views()
    logger.info(
        f"Registered on-demand feature views: "
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
