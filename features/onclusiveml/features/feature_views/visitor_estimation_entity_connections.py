"""Visitor Estimation Entity Connections."""

from datetime import timedelta

from feast import Entity, FeatureView, Field, types
from onclusiveml.features.contrib.redshift import OnclusiveRedshiftSource

# Define the entity for entity_connections
entity = Entity(name="entity_connections", join_keys=["entity_connections_id"], description="Visitor Estimation Entity Connections.")

# Define the Redshift source for the feature view
source = OnclusiveRedshiftSource(
    name="visitor_estimation_entity_connections",
    query="SELECT * FROM stage.stg_visitor_estimation__entity_connections",
    schema="stage",
    table="stg_visitor_estimation__entity_connections",
    timestamp_field="created_at",
)

# Define the feature view for entity_connections
feature_view = FeatureView(
    name="visitor_estimation_entity_connections",
    entities=[entity],
    ttl=timedelta(days=90),
    schema=[
        Field(name="child_entity_id", dtype=types.String, description="Child Entity ID."),
        Field(name="parent_entity_id", dtype=types.String, description="Parent Entity ID."),
        Field(name="type_cd", dtype=types.String, description="Type Code."),
    ],
    source=source,
)
