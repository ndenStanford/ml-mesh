"""Visitor Estimation ECLR Links."""

from datetime import timedelta

from feast import Entity, FeatureView, Field, types
from onclusiveml.features.contrib.redshift import OnclusiveRedshiftSource

# Define the entity for eclr_links
entity = Entity(name="eclr_links", join_keys=["eclr_links_id"], description="Visitor Estimation ECLR Links.")

# Define the Redshift source for the feature view
source = OnclusiveRedshiftSource(
    name="visitor_estimation_eclr_links",
    query="SELECT * FROM stage.stg_visitor_estimation__eclr_links",
    schema="stage",
    table="stg_visitor_estimation__eclr_links",
    timestamp_field="event_timestamp",
)

# Define the feature view for eclr_links
feature_view = FeatureView(
    name="visitor_estimation_eclr_links",
    entities=[entity],
    ttl=timedelta(days=10000),
    schema=[
        Field(name="entity_id", dtype=types.String, description="Entity ID."),
        Field(name="link_id", dtype=types.String, description="Link ID."),
        Field(name="link_text", dtype=types.String, description="Link Text."),
        Field(name="url", dtype=types.String, description="URL."),
        Field(name="canonical_link_id", dtype=types.String, description="Canonical Link ID."),
        Field(name="is_canonical", dtype=types.String, description="Is Canonical Link."),
    ],
    source=source,
)
