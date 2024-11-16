"""Topic features."""

from datetime import timedelta

from feast import Entity, FeatureView, Field, types
from onclusiveml.features.contrib.redshift import OnclusiveRedshiftSource

entity = Entity(name="topic", join_keys=["iptc_id"], description="Topic Entity.")

source = OnclusiveRedshiftSource(
    name="topic",
    query="SELECT * FROM features.pred_iptc_first_level",
    schema="features",
    table="pred_iptc_first_level",
    timestamp_field="created_at",
)

feature_view = FeatureView(
    name="topic_feature_view",
    entities=[entity],
    ttl=timedelta(days=90),
    schema=[
        Field(name="topic_1", dtype=types.String, description="Topic label."),
        Field(name="content", dtype=types.String, description="Content (model input)."),
        Field(name="title", dtype=types.String, description="Article title."),
        Field(name="language", dtype=types.String, description="Content Language."),
    ],
    source=source,
)
