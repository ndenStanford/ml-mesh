"""Register features for IPTC project."""

# Standard Library
from typing import Any

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSettings
from onclusiveml.core.logging import get_default_logger
from onclusiveml.core.logging.constants import OnclusiveService
from onclusiveml.data.feature_store import FeastRepoBuilder, FeatureStoreParams

# Source
from src.settings import (  # type: ignore[attr-defined]; FeatureRegistrationLLMParams,
    FeatureRegistrationParams,
    IptcFirstLevelFeatureRegistrationParams,
    IptcLLMLabelFeatureRegistrationParams,
    IptcSecondLevelFeatureRegistrationParams,
    IptcThirdLevelFeatureRegistrationParams,
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
    # feature_registration_params = FeatureRegistrationLLMParams()
    # iptc_llm_label_feature_registration_params = (
    #     IptcLLMLabelFeatureRegistrationParams()
    # )
    # register(feature_registration_params, iptc_llm_label_feature_registration_params)
def main_online():
    # Standard Library
    import json
    from typing import Dict, List

    # 3rd party libraries
    import pandas as pd
    import requests
    from feast import Field
    # from src.settings import get_settings
    from feast.on_demand_feature_view import on_demand_feature_view
    from feast.types import String

    # Internal libraries
    from onclusiveml.core.base import OnclusiveFrozenSettings

    feature_registration_params = FeatureRegistrationParams()
    # settings = get_settings()
    class PromptBackendAPISettings:
        """API configuration."""

        PROMPT_API: str = "http://prompt-backend:4000"
        INTERNAL_ML_ENDPOINT_API_KEY: str = "1234"
        CLAUDE_IPTC_ALIAS: str = "ml-iptc-topic-prediction"

        IPTC_RESPONSE_SCHEMA: Dict[str, str] = {
            "iptc category": "Answer the IPTC category",
            "reason": "The reason for why you think it is this category",  # noqa: E501
        }
        DEFAULT_MODEL: str = "anthropic.claude-3-5-sonnet-20240620-v1:0"

    settings = PromptBackendAPISettings()

    title = (
        "Tesla, Inc. is an American multinational automotive and clean energy company."
    )
    article = """Tesla, Inc. is an American multinational automotive and clean energy company. Headquartered in Austin, Texas, it designs, manufactures and sells battery electric vehicles, stationary battery energy storage devices from home to grid-scale, solar panels and solar shingles, and related products and services."""
    candidates = [
        {
            "name": "arts, culture, entertainment and media",
            "description": "All forms of arts, entertainment, cultural heritage and media",
        },
        {
            "name": "cinema",
            "description": "Stories told through motion pictures, such as full-length or short format documentary or fictional features",
        },
    ]

    def generate_label_llm(title, article, candidates):
        input_dict = {
            "input": {"title": title, "article": article, "candidates": candidates},
            "output": settings.IPTC_RESPONSE_SCHEMA,
        }
        headers = {"x-api-key": settings.INTERNAL_ML_ENDPOINT_API_KEY}
        q = requests.post(
            "{}/api/v2/prompts/{}/generate/model/{}".format(
                settings.PROMPT_API, settings.CLAUDE_IPTC_ALIAS, settings.DEFAULT_MODEL
            ),
            headers=headers,
            json=input_dict,
        )
        output_content = json.loads(q.content)
        return output_content["iptc category"]
    # def generate_label_llm(title, article, candidates):
    #     return (title+article)
    # def generate_label_llm(title, article):
    #     return (title+article)
    # def identity(n):
    #     return n
    feast_repo_builder = FeastRepoBuilder(feature_registration_params)
    fs_handle = feast_repo_builder.fs_handle
    # fs_handle = FeatureStoreHandle(
    #     feast_config_bucket=settings.feast_config_bucket,
    #     config_file=settings.config_file,
    #     local_config_dir=settings.local_config_dir,
    #     data_source=settings.redshift_table,
    #     data_id_key=settings.entity_join_key,
    #     limit=settings.n_records_full,
    # )
    feature_view = [
        feature_view
        for feature_view in fs_handle.list_feature_views()
        if feature_view.name == "iptc_first_level_feature_view"
    ][0]

    print(fs_handle.list_feature_views())
    # @on_demand_feature_view(
    #     sources=[feature_view],  # CHANGE TO FEATURE VIEW OBJECT
    #     schema=[
    #         Field(name="topic_1_llm", dtype=String),
    #     ],
    # )
    def iptc_llm_feature_view_2(features_df: pd.DataFrame) -> pd.DataFrame:
        candidates = [
            {
                "name": "arts, culture, entertainment and media",
                "description": "All forms of arts, entertainment, cultural heritage and media",
            },
            {
                "name": "cinema",
                "description": "Stories told through motion pictures, such as full-length or short format documentary or fictional features",
            },
        ]

        df = pd.DataFrame()
        topic_label = [
            generate_label_llm(title, content, candidates)
            # (title+content)
            for title, content in zip(
                features_df["title"].values, features_df["content"].values
            )
        ]
        df["topic_1_llm"] = pd.Series(topic_label).astype(pd.StringDtype())
        # df["topic_1_llm"] = features_df["title"].astype(pd.StringDtype())
        return df
    # 3rd party libraries
    from feast import Entity, FeatureView, Field, OnDemandFeatureView

    # Internal libraries
    from onclusiveml.data.feature_store import (
        FeatureStoreHandle,
        RedshiftSourceCustom,
    )

    # data_source = RedshiftSourceCustom(
    #     table="iptc_llm_label",
    #     timestamp_field="event_timestamp",
    #     database="sources_dev",
    #     schema="feast",
    # )
    # 3rd party libraries
    # no_entity_feature_view = FeatureView(
    #             # The unique name of this feature view. Two feature views in a single
    #             # project cannot have the same name
    #             name='iptc_llm_feature_view_2',
    #             # The list of features defined below act as a schema to both define features
    #             # for both materialization of features into a store, and are used as references
    #             # during retrieval for building a training dataset or serving features
    #             schema=[Field(name='topic_1_llm', dtype=String)],
    #             online=False,
    #             source=data_source,
    #             # Tags are user defined key/value pairs that are attached to each
    #             # feature view
    #             tags={},
    #         )
    from feast.types import PrimitiveFeastType

    no_entity_feature_view = OnDemandFeatureView(
        name="iptc_llm_feature_view_2",
        sources=[fs_handle.fs.get_feature_view("iptc_first_level_feature_view")],
        schema=[Field(name="topic_1_llm", dtype=String)],
        # schema=["topic_1_llm-String"],
        udf=iptc_llm_feature_view_2,
    )
    # no_entity_feature_view = OnDemandFeatureView(
    #     name='iptc_llm_feature_view_2',
    #     sources=[fs_handle.fs.get_feature_view('iptc_first_level_feature_view')],
    #     schema=[Field(name='topic_1_llm', dtype=ValueType.STRING)],
    #     # schema=["topic_1_llm-String"],
    #     udf=iptc_llm_feature_view_2
    # )
    # y=no_entity_feature_view.infer_features()
    x = fs_handle.register([no_entity_feature_view])
    print("finish register online feature")

    features = [
        f"{feature_view.name}:{feature.name}" for feature in feature_view.features
    ]
    # features += [
    #     computed_feature_name for computed_feature_name in settings.computed_features
    # ]
    features += ["iptc_llm_feature_view_2:topic_1_llm"]
    # entity_df="""SELECT title, content, iptc_id, CURRENT_TIMESTAMP AS event_timestamp FROM "feast"."iptc_first_level"
    # LIMIT 10"""
    entity_df = """SELECT iptc_id, CURRENT_TIMESTAMP AS event_timestamp FROM "feast"."iptc_first_level"
    LIMIT 10"""

    dataset_df = fs_handle.fs.get_historical_features(
        entity_df=entity_df, features=features
    )
    df = dataset_df.to_df()
    print(df)


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

    plan_repo_contents(feast_repo_builder)

    if feature_registration_params.register_features:
        register_repo_contents(feast_repo_builder)


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
    main_online()
