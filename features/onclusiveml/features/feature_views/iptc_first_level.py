"""Iptc first level."""

from datetime import timedelta

from feast import Entity, FeatureView, Field, types
from onclusiveml.features.contrib.redshift import OnclusiveRedshiftSource

entity = Entity(name="iptc_first_level", join_keys=["iptc_id"], description="Iptc First Level.")

source = OnclusiveRedshiftSource(
    name="iptc_first_level",
    query="SELECT * FROM features.pred_iptc_first_level",
    schema="features",
    table="pred_iptc_first_level",
    timestamp_field="created_at",
)

feature_view = FeatureView(
    name="iptc_first_level",
    entities=[entity],
    ttl=timedelta(days=90),
    schema=[
        Field(name="topic_1", dtype=types.String, description="Level 1 IPTC Topic label."),
        Field(name="content", dtype=types.String, description="Content (model input)."),
        Field(name="title", dtype=types.String, description="Article title."),
        Field(name="language", dtype=types.String, description="Content Language."),
    ],
    source=source,
)
