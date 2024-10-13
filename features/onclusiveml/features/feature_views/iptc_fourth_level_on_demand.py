"""Iptc fourth level."""

from feast import Field, OnDemandFeatureView, types
from feast.transformation.pandas_transformation import PandasTransformation
from onclusiveml.features.contrib.on_demand.iptc.utils import iptc_fourth_level_on_demand_feature_view
from onclusiveml.features.feature_views.iptc_third_level import feature_view

feature_transformation = PandasTransformation(
    udf=iptc_fourth_level_on_demand_feature_view,
    udf_string="iptc_fourth_level_on_demand_feature_view",
)

feature_view = OnDemandFeatureView(
    name="iptc_fourth_level_on_demand_feature_view",
    sources=[feature_view],
    schema=[Field(name="topic_4_llm", dtype=types.String, description="")],
    feature_transformation=feature_transformation,
)
