"""Visitor Estimation Search Seeds."""

from datetime import timedelta

from feast import Entity, FeatureView, Field, types
from onclusiveml.features.contrib.redshift import OnclusiveRedshiftSource

# Define the entity for search_seeds
entity = Entity(name="search_seeds", join_keys=["search_seeds_id"], description="Visitor Estimation Search Seeds.")

# Define the Redshift source for the feature view
source = OnclusiveRedshiftSource(
    name="visitor_estimation_search_seeds",
    query="SELECT * FROM stage.stg_visitor_estimation__search_seeds",
    schema="stage",
    table="stg_visitor_estimation__search_seeds",
    timestamp_field="created_at",
)

# Define the feature view for search_seeds
feature_view = FeatureView(
    name="visitor_estimation_search_seeds",
    entities=[entity],
    ttl=timedelta(days=90),
    schema=[
        Field(name="profile_id", dtype=types.String, description="Profile ID."),
        Field(name="name", dtype=types.String, description="Name."),
        Field(name="remove_suffix", dtype=types.String, description="Remove Suffix."),
        Field(name="add_parent_company_name", dtype=types.String, description="Add Parent Company Name."),
        Field(name="seed_type_cd", dtype=types.String, description="Seed Type Code."),
        Field(name="case_sensitive", dtype=types.String, description="Is Case Sensitive."),
        Field(name="updated_at", dtype=types.String, description="Updated At."),
        Field(name="created_at", dtype=types.String, description="Created At."),
    ],
    source=source,
)
