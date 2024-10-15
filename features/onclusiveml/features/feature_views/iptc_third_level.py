"""Iptc third level."""

from datetime import timedelta

from feast import Entity, FeatureView, Field, types, OnDemandFeatureView
from onclusiveml.features.contrib.redshift import OnclusiveRedshiftSource
from feast.transformation.pandas_transformation import PandasTransformation
from onclusiveml.features.contrib.on_demand.iptc.utils import iptc_third_level_on_demand_feature_view
from onclusiveml.features.feature_views.iptc_third_level import feature_view

entity = Entity(
    name="iptc_third_level",
    join_keys=["iptc_id"],
    description="Iptc Third level.",
)

source = OnclusiveRedshiftSource(
    name="iptc_third_level",
    query="SELECT * FROM features.pred_iptc_third_level",
    schema="features",
    table="pred_iptc_third_level",
    timestamp_field="created_at",
)

feature_view = FeatureView(
    name="iptc_third_level",
    entities=[entity],
    ttl=timedelta(days=90),
    schema=[
        Field(name="topic_1", dtype=types.String, description="Level 1 IPTC Topic label."),
        Field(name="topic_2", dtype=types.String, description="Level 2 IPTC Topic label."),
        Field(name="topic_3", dtype=types.String, description="Level 3 IPTC Topic label."),
        Field(name="content", dtype=types.String, description="Content (model input)."),
        Field(name="title", dtype=types.String, description="Article title."),
        Field(name="language", dtype=types.String, description="Content Language."),
    ],
    source=source,
)


feature_transformation = PandasTransformation(
    udf=iptc_third_level_on_demand_feature_view,
    udf_string="iptc_third_level_on_demand_feature_view",
)

on_demand_feature_view = OnDemandFeatureView(
    name="iptc_third_level_on_demand_feature_view",
    sources=[feature_view],
    schema=[Field(name="topic_3_llm", dtype=types.String, description="")],
    feature_transformation=feature_transformation,
)
