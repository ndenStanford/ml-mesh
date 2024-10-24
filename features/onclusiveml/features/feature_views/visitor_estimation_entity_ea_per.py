"""Visitor Estimation Entity EA Per."""

from datetime import timedelta

from feast import Entity, FeatureView, Field, types
from onclusiveml.features.contrib.redshift import OnclusiveRedshiftSource

# Define the entity for entity_ea_per
entity = Entity(name="entity_ea_per", join_keys=["entity_ea_per_id"], description="Visitor Estimation Entity EA Per.")

# Define the Redshift source for the feature view
source = OnclusiveRedshiftSource(
    name="visitor_estimation_entity_ea_per",
    query="SELECT * FROM stage.stg_visitor_estimation__entity_ea_per",
    schema="stage",
    table="stg_visitor_estimation__entity_ea_per",
    timestamp_field="created_at",
)

# Define the feature view for entity_ea_per
feature_view = FeatureView(
    name="visitor_estimation_entity_ea_per",
    entities=[entity],
    ttl=timedelta(days=90),
    schema=[
        Field(name="profile_id", dtype=types.String, description="Profile ID."),
        Field(name="entity_id", dtype=types.String, description="Entity ID."),
        Field(name="ea_timestamp", dtype=types.String, description="EA Timestamp."),
        Field(name="link_visitors", dtype=types.String, description="Link Visitors."),
        Field(name="secondsLag", dtype=types.String, description="Seconds Lag."),
    ],
    source=source,
)
