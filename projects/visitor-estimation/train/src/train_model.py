"""Train IPTC model."""

# Internal libraries
from onclusiveml.core.logging import get_default_logger

# Source
from src.settings import (  # type: ignore[attr-defined]
    CrawlerItemsDataFetchParams,
    DataFetchParams,
    DomainsDataFetchParams,
    EclrLinksDataFetchParams,
    EntityConnectionsDataFetchParams,
    EntityEaPerDataFetchParams,
    EntityLinksDataFetchParams,
    EntityLinksLmdDataFetchParams,
    ProfileCompanySectorsDataFetchParams,
    ProfileEntityRelationshipsDataFetchParams,
    SearchSeedsDataFetchParams,
    TrackedVEBaseModelCard,
    TrackedVEModelSpecs,
)
from src.trainer import VisitorEstimationTrainer


logger = get_default_logger(__name__)


def main() -> None:
    """Execute the training process."""
    model_specs = TrackedVEModelSpecs()
    model_card = TrackedVEBaseModelCard()
    data_fetch_params = DataFetchParams()

    trainer = VisitorEstimationTrainer(model_specs, model_card, data_fetch_params)

    # create the dataset dictionary
    for params in [
        CrawlerItemsDataFetchParams(),
        EclrLinksDataFetchParams(),
        EntityConnectionsDataFetchParams(),
        EntityEaPerDataFetchParams(),
        EntityLinksLmdDataFetchParams(),
        EntityLinksDataFetchParams(),
        ProfileCompanySectorsDataFetchParams(),
        SearchSeedsDataFetchParams(),
        DomainsDataFetchParams(),
        ProfileEntityRelationshipsDataFetchParams(),
    ]:
        data_fetch_configurations = {
            "crawler_items": {
                "entity_df": """ SELECT crawler_items_id, CURRENT_TIMESTAMP AS event_timestamp FROM "stage"."stg_visitor_estimation__crawler_items" """,
                "features": [
                    "visitor_estimation_crawler_items:entity_id",
                    "visitor_estimation_crawler_items:word_count",
                    "visitor_estimation_crawler_items:extracted_entities",
                    "visitor_estimation_crawler_items:url",
                ],
            },
            "eclr_links": {
                "entity_df": """ SELECT eclr_links_id, CURRENT_TIMESTAMP AS event_timestamp FROM "stage"."stg_visitor_estimation__eclr_links" """,
                "features": [
                    "visitor_estimation_eclr_links:entity_id",
                    "visitor_estimation_eclr_links:link_id",
                    "visitor_estimation_eclr_links:link_text",
                    "visitor_estimation_eclr_links:url",
                    "visitor_estimation_eclr_links:canonical_link_id",
                    "visitor_estimation_eclr_links:is_canonical",
                ],
            },
            "entity_connections": {
                "entity_df": """ SELECT entity_connections_id, CURRENT_TIMESTAMP AS event_timestamp FROM "stage"."stg_visitor_estimation__entity_connections" """,
                "features": [
                    "visitor_estimation_entity_connections:child_entity_id",
                    "visitor_estimation_entity_connections:parent_entity_id",
                    "visitor_estimation_entity_connections:type_cd",
                ],
            },
            "entity_ea_per": {
                "entity_df": """ SELECT entity_ea_per_id, CURRENT_TIMESTAMP AS event_timestamp FROM "stage"."stg_visitor_estimation__entity_ea_per" """,
                "features": [
                    "visitor_estimation_entity_ea_per:profile_id",
                    "visitor_estimation_entity_ea_per:entity_id",
                    "visitor_estimation_entity_ea_per:ea_timestamp",
                    "visitor_estimation_entity_ea_per:link_visitors",
                    "visitor_estimation_entity_ea_per:secondsLag",
                ],
            },
            "entity_links_lmd": {
                "entity_df": """ SELECT entity_links_lmd_id, CURRENT_TIMESTAMP AS event_timestamp FROM "stage"."stg_visitor_estimation__entity_links_metadata" """,
                "features": [
                    "visitor_estimation_entity_links_lmd:entity_id",
                    "visitor_estimation_entity_links_lmd:link_metadata_timestamp",
                    "visitor_estimation_entity_links_lmd:fb_likes",
                    "visitor_estimation_entity_links_lmd:fb_comments",
                    "visitor_estimation_entity_links_lmd:fb_shares",
                    "visitor_estimation_entity_links_lmd:fb_total",
                    "visitor_estimation_entity_links_lmd:fb_clicks",
                    "visitor_estimation_entity_links_lmd:twitter_retweets",
                    "visitor_estimation_entity_links_lmd:google_plusones",
                    "visitor_estimation_entity_links_lmd:linkedin_shares",
                    "visitor_estimation_entity_links_lmd:twitter_favorites",
                    "visitor_estimation_entity_links_lmd:google_reshares",
                    "visitor_estimation_entity_links_lmd:google_replies",
                ],
            },
            "entity_links": {
                "entity_df": """ SELECT entity_links_id, CURRENT_TIMESTAMP AS event_timestamp FROM "stage"."stg_visitor_estimation__entity_links" """,
                "features": [
                    "visitor_estimation_entity_links:entity_id",
                    "visitor_estimation_entity_links:link_id",
                    "visitor_estimation_entity_links:entities_entity_timestamp",
                    "visitor_estimation_entity_links:domain_id",
                    "visitor_estimation_entity_links:type_cd",
                    "visitor_estimation_entity_links:article_type_cd",
                    "visitor_estimation_entity_links:language",
                    "visitor_estimation_entity_links:language_reliable",
                    "visitor_estimation_entity_links:pagerank",
                ],
            },
            "profile_company_sectors": {
                "entity_df": """ SELECT profile_company_sectors_id, CURRENT_TIMESTAMP AS event_timestamp FROM "stage"."stg_visitor_estimation__profile_company_sectors" """,
                "features": [
                    "visitor_estimation_profile_company_sectors:profile_id",
                    "visitor_estimation_profile_company_sectors:url",
                    "visitor_estimation_profile_company_sectors:company_name",
                    "visitor_estimation_profile_company_sectors:enabled",
                    "visitor_estimation_profile_company_sectors:start_date",
                    "visitor_estimation_profile_company_sectors:onboarding_validations",
                    "visitor_estimation_profile_company_sectors:parent_id",
                    "visitor_estimation_profile_company_sectors:is_customer",
                    "visitor_estimation_profile_company_sectors:analytics_profile_id",
                    "visitor_estimation_profile_company_sectors:company_sector_id",
                    "visitor_estimation_profile_company_sectors:category_id",
                    "visitor_estimation_profile_company_sectors:is_category",
                ],
            },
            "search_seeds": {
                "entity_df": """ SELECT search_seeds_id, CURRENT_TIMESTAMP AS event_timestamp FROM "stage"."stg_visitor_estimation__search_seeds" """,
                "features": [
                    "visitor_estimation_search_seeds:profile_id",
                    "visitor_estimation_search_seeds:name",
                    "visitor_estimation_search_seeds:remove_suffix",
                    "visitor_estimation_search_seeds:add_parent_company_name",
                    "visitor_estimation_search_seeds:seed_type_cd",
                    "visitor_estimation_search_seeds:case_sensitive",
                    "visitor_estimation_search_seeds:updated_at",
                    "visitor_estimation_search_seeds:created_at",
                ],
            },
            "domains": {
                "entity_df": """ SELECT domains_id, CURRENT_TIMESTAMP AS event_timestamp FROM "stage"."stg_visitor_estimation__domains" """,
                "features": [
                    "visitor_estimation_domains:tld",
                    "visitor_estimation_domains:publication",
                    "visitor_estimation_domains:name",
                    "visitor_estimation_domains:pagerank",
                    "visitor_estimation_domains:social_modifier",
                    "visitor_estimation_domains:id",
                    "visitor_estimation_domains:article_type_cd",
                    "visitor_estimation_domains:subdomain",
                    "visitor_estimation_domains:country",
                ],
            },
            "profile_entity_relationships": {
                "entity_df": """ SELECT per_id, CURRENT_TIMESTAMP AS event_timestamp FROM "stage"."stg_visitor_estimation__profile_entity_relationships" """,
                "features": [
                    "visitor_estimation_profile_entity_relationships:id",
                    "visitor_estimation_profile_entity_relationships:profile_id",
                    "visitor_estimation_profile_entity_relationships:entity_id",
                    "visitor_estimation_profile_entity_relationships:relevance_score",
                    "visitor_estimation_profile_entity_relationships:owned_media_flag",
                    "visitor_estimation_profile_entity_relationships:link_present_flag",
                    "visitor_estimation_profile_entity_relationships:analytics_flag",
                    "visitor_estimation_profile_entity_relationships:updated_at",
                    "visitor_estimation_profile_entity_relationships:created_at",
                ],
            },
        }

        trainer.data_fetch_params.entity_name = params.entity_name
        trainer.data_fetch_params.entity_join_key = params.entity_join_key
        trainer.data_fetch_params.redshift_table = params.redshift_table
        trainer.data_fetch_params.feature_view_name = params.feature_view_name
        trainer.data_fetch_params.entity_df = data_fetch_configurations[
            params.entity_name
        ]["entity_df"]
        trainer.data_fetch_params.features = data_fetch_configurations[
            params.entity_name
        ]["features"]
        trainer.build_dataset_dict()
    logger.info("Dataset dictionary creation complete.")

    # Start the training and register models to neptune
    trainer()


if __name__ == "__main__":
    main()
