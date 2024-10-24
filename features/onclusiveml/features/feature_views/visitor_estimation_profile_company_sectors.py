"""Visitor Estimation Profile Company Sectors."""

from datetime import timedelta

from feast import Entity, FeatureView, Field, types
from onclusiveml.features.contrib.redshift import OnclusiveRedshiftSource

# Define the entity for profile_company_sectors
entity = Entity(name="profile_company_sectors", join_keys=["profile_company_sectors_id"], description="Visitor Estimation Profile Company Sectors.")

# Define the Redshift source for the feature view
source = OnclusiveRedshiftSource(
    name="visitor_estimation_profile_company_sectors",
    query="SELECT * FROM stage.stg_visitor_estimation__profile_company_sectors",
    schema="stage",
    table="stg_visitor_estimation__profile_company_sectors",
    timestamp_field="event_timestamp",
)

# Define the feature view for profile_company_sectors
feature_view = FeatureView(
    name="visitor_estimation_profile_company_sectors",
    entities=[entity],
    ttl=timedelta(days=10000),
    schema=[
        Field(name="profile_id", dtype=types.String, description="Profile ID."),
        Field(name="url", dtype=types.String, description="URL."),
        Field(name="company_name", dtype=types.String, description="Company Name."),
        Field(name="enabled", dtype=types.String, description="Is Enabled."),
        Field(name="start_date", dtype=types.String, description="Start Date."),
        Field(name="onboarding_validations", dtype=types.String, description="Onboarding Validations."),
        Field(name="parent_id", dtype=types.String, description="Parent ID."),
        Field(name="is_customer", dtype=types.String, description="Is Customer."),
        Field(name="analytics_profile_id", dtype=types.String, description="Analytics Profile ID."),
        Field(name="company_sector_id", dtype=types.String, description="Company Sector ID."),
        Field(name="category_id", dtype=types.String, description="Category ID."),
        Field(name="is_category", dtype=types.String, description="Is Category."),
    ],
    source=source,
)
