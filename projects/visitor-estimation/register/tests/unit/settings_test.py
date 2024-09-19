"""Settings test."""

# Source
from src.settings import (
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


def test_feature_registration_params():
    """Test default FeatureRegistrationParams."""
    feature_registration_params = FeatureRegistrationParams()
    assert feature_registration_params.redshift_table == "visitor-estimation"
    assert feature_registration_params.entity_name == "visitor-estimation"
    assert (
        feature_registration_params.feature_view_name
        == "visitor_estimation_feature_view"
    )
    assert feature_registration_params.entity_join_key == "visitor_estimation_id"
    assert feature_registration_params.register_features is False
    assert feature_registration_params.timestamp_field == "event_timestamp"


def test_crawler_items_feature_registration_params():
    """Test default CrawlerItemsFeatureRegistrationParams."""
    crawler_params = CrawlerItemsFeatureRegistrationParams(
        entity_name="crawler_entity",
        feature_view_name="crawler_view",
        redshift_table="crawler_table",
        fields=[("field1", "string")],
        join_key="crawler_join_key",
    )
    assert crawler_params.entity_name == "crawler_entity"
    assert crawler_params.feature_view_name == "crawler_view"
    assert crawler_params.redshift_table == "crawler_table"
    assert crawler_params.fields == [("field1", "string")]
    assert crawler_params.join_key == "crawler_join_key"


def test_eclr_links_feature_registration_params():
    """Test default EclrLinksFeatureRegistrationParams."""
    eclr_params = EclrLinksFeatureRegistrationParams(
        entity_name="eclr_entity",
        feature_view_name="eclr_view",
        redshift_table="eclr_table",
        fields=[("field1", "string")],
        join_key="eclr_join_key",
    )
    assert eclr_params.entity_name == "eclr_entity"
    assert eclr_params.feature_view_name == "eclr_view"
    assert eclr_params.redshift_table == "eclr_table"
    assert eclr_params.fields == [("field1", "string")]
    assert eclr_params.join_key == "eclr_join_key"


def test_entity_connections_feature_registration_params():
    """Test default EntityConnectionsFeatureRegistrationParams."""
    entity_connections_params = EntityConnectionsFeatureRegistrationParams(
        entity_name="entity_connections_entity",
        feature_view_name="entity_connections_view",
        redshift_table="entity_connections_table",
        fields=[("field1", "string")],
        join_key="entity_connections_join_key",
    )
    assert entity_connections_params.entity_name == "entity_connections_entity"
    assert entity_connections_params.feature_view_name == "entity_connections_view"
    assert entity_connections_params.redshift_table == "entity_connections_table"
    assert entity_connections_params.fields == [("field1", "string")]
    assert entity_connections_params.join_key == "entity_connections_join_key"


def test_entity_ea_per_feature_registration_params():
    """Test default EntityEaPerFeatureRegistrationParams."""
    entity_ea_per_params = EntityEaPerFeatureRegistrationParams(
        entity_name="entity_ea_per_entity",
        feature_view_name="entity_ea_per_view",
        redshift_table="entity_ea_per_table",
        fields=[("field1", "string")],
        join_key="entity_ea_per_join_key",
    )
    assert entity_ea_per_params.entity_name == "entity_ea_per_entity"
    assert entity_ea_per_params.feature_view_name == "entity_ea_per_view"
    assert entity_ea_per_params.redshift_table == "entity_ea_per_table"
    assert entity_ea_per_params.fields == [("field1", "string")]
    assert entity_ea_per_params.join_key == "entity_ea_per_join_key"


def test_entity_links_lmd_feature_registration_params():
    """Test default EntityLinksLmdFeatureRegistrationParams."""
    entity_links_lmd_params = EntityLinksLmdFeatureRegistrationParams(
        entity_name="entity_links_lmd_entity",
        feature_view_name="entity_links_lmd_view",
        redshift_table="entity_links_lmd_table",
        fields=[("field1", "string")],
        join_key="entity_links_lmd_join_key",
    )
    assert entity_links_lmd_params.entity_name == "entity_links_lmd_entity"
    assert entity_links_lmd_params.feature_view_name == "entity_links_lmd_view"
    assert entity_links_lmd_params.redshift_table == "entity_links_lmd_table"
    assert entity_links_lmd_params.fields == [("field1", "string")]
    assert entity_links_lmd_params.join_key == "entity_links_lmd_join_key"


def test_entity_links_feature_registration_params():
    """Test default EntityLinksFeatureRegistrationParams."""
    entity_links_params = EntityLinksFeatureRegistrationParams(
        entity_name="entity_links_entity",
        feature_view_name="entity_links_view",
        redshift_table="entity_links_table",
        fields=[("field1", "string")],
        join_key="entity_links_join_key",
    )
    assert entity_links_params.entity_name == "entity_links_entity"
    assert entity_links_params.feature_view_name == "entity_links_view"
    assert entity_links_params.redshift_table == "entity_links_table"
    assert entity_links_params.fields == [("field1", "string")]
    assert entity_links_params.join_key == "entity_links_join_key"


def test_profile_company_sectors_feature_registration_params():
    """Test default ProfileCompanySectorsFeatureRegistrationParams."""
    profile_company_sectors_params = ProfileCompanySectorsFeatureRegistrationParams(
        entity_name="profile_company_sectors_entity",
        feature_view_name="profile_company_sectors_view",
        redshift_table="profile_company_sectors_table",
        fields=[("field1", "string")],
        join_key="profile_company_sectors_join_key",
    )
    assert (
        profile_company_sectors_params.entity_name == "profile_company_sectors_entity"
    )
    assert (
        profile_company_sectors_params.feature_view_name
        == "profile_company_sectors_view"
    )
    assert (
        profile_company_sectors_params.redshift_table == "profile_company_sectors_table"
    )
    assert profile_company_sectors_params.fields == [("field1", "string")]
    assert profile_company_sectors_params.join_key == "profile_company_sectors_join_key"


def test_search_seeds_feature_registration_params():
    """Test default SearchSeedsFeatureRegistrationParams."""
    search_seeds_params = SearchSeedsFeatureRegistrationParams(
        entity_name="search_seeds_entity",
        feature_view_name="search_seeds_view",
        redshift_table="search_seeds_table",
        fields=[("field1", "string")],
        join_key="search_seeds_join_key",
    )
    assert search_seeds_params.entity_name == "search_seeds_entity"
    assert search_seeds_params.feature_view_name == "search_seeds_view"
    assert search_seeds_params.redshift_table == "search_seeds_table"
    assert search_seeds_params.fields == [("field1", "string")]
    assert search_seeds_params.join_key == "search_seeds_join_key"


def test_domains_feature_registration_params():
    """Test default DomainsFeatureRegistrationParams."""
    domains_params = DomainsFeatureRegistrationParams(
        entity_name="domains_entity",
        feature_view_name="domains_view",
        redshift_table="domains_table",
        fields=[("field1", "string")],
        join_key="domains_join_key",
    )
    assert domains_params.entity_name == "domains_entity"
    assert domains_params.feature_view_name == "domains_view"
    assert domains_params.redshift_table == "domains_table"
    assert domains_params.fields == [("field1", "string")]
    assert domains_params.join_key == "domains_join_key"


def test_profile_entity_relationships_feature_registration_params():
    """Test default ProfileEntityRelationshipsFeatureRegistrationParams."""
    profile_entity_relationships_params = (
        ProfileEntityRelationshipsFeatureRegistrationParams(
            entity_name="profile_entity_relationships_entity",
            feature_view_name="profile_entity_relationships_view",
            redshift_table="profile_entity_relationships_table",
            fields=[("field1", "string")],
            join_key="profile_entity_relationships_join_key",
        )
    )
    assert (
        profile_entity_relationships_params.entity_name
        == "profile_entity_relationships_entity"
    )
    assert (
        profile_entity_relationships_params.feature_view_name
        == "profile_entity_relationships_view"
    )
    assert (
        profile_entity_relationships_params.redshift_table
        == "profile_entity_relationships_table"
    )
    assert profile_entity_relationships_params.fields == [("field1", "string")]
    assert (
        profile_entity_relationships_params.join_key
        == "profile_entity_relationships_join_key"
    )
