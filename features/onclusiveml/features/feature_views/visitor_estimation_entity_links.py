"""Visitor Estimation Entity Links."""

from datetime import timedelta

from feast import Entity, FeatureView, Field, types
from onclusiveml.features.contrib.redshift import OnclusiveRedshiftSource

# Define the entity for entity_links
entity = Entity(name="entity_links", join_keys=["entity_links_id"], description="Visitor Estimation Entity Links.")

# Define the Redshift source for the feature view
source = OnclusiveRedshiftSource(
    name="visitor_estimation_entity_links",
    query="SELECT * FROM stage.stg_visitor_estimation__entity_links",
    schema="stage",
    table="stg_visitor_estimation__entity_links",
    timestamp_field="created_at",
)

# Define the feature view for entity_links
feature_view = FeatureView(
    name="visitor_estimation_entity_links",
    entities=[entity],
    ttl=timedelta(days=90),
    schema=[
        Field(name="entity_id", dtype=types.String, description="Entity ID."),
        Field(name="link_id", dtype=types.String, description="Link ID."),
        Field(name="entities_entity_timestamp", dtype=types.String, description="Entities Entity Timestamp."),
        Field(name="domain_id", dtype=types.String, description="Domain ID."),
        Field(name="type_cd", dtype=types.String, description="Type Code."),
        Field(name="article_type_cd", dtype=types.String, description="Article Type Code."),
        Field(name="language", dtype=types.String, description="Language."),
        Field(name="language_reliable", dtype=types.String, description="Is Language Reliable."),
        Field(name="pagerank", dtype=types.String, description="PageRank."),
    ],
    source=source,
)
