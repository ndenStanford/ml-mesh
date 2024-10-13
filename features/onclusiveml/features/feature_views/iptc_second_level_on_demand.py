"""Iptc second level."""

from feast import Field, OnDemandFeatureView, types
from feast.transformation.pandas_transformation import PandasTransformation
from onclusiveml.features.contrib.on_demand.iptc.utils import iptc_second_level_on_demand_feature_view
from onclusiveml.features.feature_views.iptc_second_level import feature_view

feature_transformation = PandasTransformation(
    udf=iptc_second_level_on_demand_feature_view,
    udf_string="iptc_second_level_on_demand_feature_view",
)

feature_view = OnDemandFeatureView(
    name="iptc_second_level_on_demand_feature_view",
    sources=[feature_view],
    schema=[Field(name="topic_2_llm", dtype=types.String, description="")],
    feature_transformation=feature_transformation,
)
