"""Visitor Estimation Profile Entity Relationships."""

from datetime import timedelta

from feast import Entity, FeatureView, Field, types
from onclusiveml.features.contrib.redshift import OnclusiveRedshiftSource

# Define the entity for profile_entity_relationships
entity = Entity(name="profile_entity_relationships", join_keys=["per_id"], description="Visitor Estimation Profile Entity Relationships.")

# Define the Redshift source for the feature view
source = OnclusiveRedshiftSource(
    name="visitor_estimation_profile_entity_relationships",
    query="SELECT * FROM stage.stg_visitor_estimation__profile_entity_relationships",
    schema="stage",
    table="stg_visitor_estimation__profile_entity_relationships",
    timestamp_field="created_at",
)

# Define the feature view for profile_entity_relationships
feature_view = FeatureView(
    name="visitor_estimation_profile_entity_relationships",
    entities=[entity],
    ttl=timedelta(days=90),
    schema=[
        Field(name="id", dtype=types.String, description="ID."),
        Field(name="profile_id", dtype=types.String, description="Profile ID."),
        Field(name="entity_id", dtype=types.String, description="Entity ID."),
        Field(name="relevance_score", dtype=types.String, description="Relevance Score."),
        Field(name="owned_media_flag", dtype=types.String, description="Owned Media Flag."),
        Field(name="link_present_flag", dtype=types.String, description="Link Present Flag."),
        Field(name="analytics_flag", dtype=types.String, description="Analytics Flag."),
        Field(name="updated_at", dtype=types.String, description="Updated At."),
        Field(name="created_at", dtype=types.String, description="Created At."),
    ],
    source=source,
)
