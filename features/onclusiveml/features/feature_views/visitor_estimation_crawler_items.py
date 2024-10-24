"""Visitor Estimation Crawler Items."""

from datetime import timedelta

from feast import Entity, FeatureView, Field, types
from onclusiveml.features.contrib.redshift import OnclusiveRedshiftSource

entity = Entity(name="crawler_items", join_keys=["crawler_items_id"], description="Visitor Estimation Crawler Items.")

source = OnclusiveRedshiftSource(
    name="visitor_estimation_crawler_items",
    query="SELECT * FROM stage.stg_visitor_estimation__crawler_items",
    schema="stage",
    table="stg_visitor_estimation__crawler_items",
    timestamp_field="created_at",
)

feature_view = FeatureView(
    name="visitor_estimation_crawler_items",
    entities=[entity],
    ttl=timedelta(days=90),
    schema=[
        Field(name="entity_id", dtype=types.String, description="Entity ID."),
        Field(name="word_count", dtype=types.String, description="Word Count."),
        Field(name="extracted_entities", dtype=types.String, description="Extracted Entities."),
        Field(name="url", dtype=types.String, description="URL."),
    ],
    source=source,
)
