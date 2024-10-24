"""Visitor Estimation Domains."""

from datetime import timedelta

from feast import Entity, FeatureView, Field, types
from onclusiveml.features.contrib.redshift import OnclusiveRedshiftSource

# Define the entity for domains
entity = Entity(name="domains", join_keys=["domains_id"], description="Visitor Estimation Domains.")

# Define the Redshift source for the feature view
source = OnclusiveRedshiftSource(
    name="visitor_estimation_domains",
    query="SELECT * FROM stage.stg_visitor_estimation__domains",
    schema="stage",
    table="stg_visitor_estimation__domains",
    timestamp_field="event_timestamp",
)

# Define the feature view for domains
feature_view = FeatureView(
    name="visitor_estimation_domains",
    entities=[entity],
    ttl=timedelta(days=10000),
    schema=[
        Field(name="tld", dtype=types.String, description="Top-Level Domain."),
        Field(name="publication", dtype=types.String, description="Publication."),
        Field(name="name", dtype=types.String, description="Name."),
        Field(name="pagerank", dtype=types.String, description="PageRank."),
        Field(name="social_modifier", dtype=types.String, description="Social Modifier."),
        Field(name="id", dtype=types.String, description="Domain ID."),
        Field(name="article_type_cd", dtype=types.String, description="Article Type Code."),
        Field(name="subdomain", dtype=types.String, description="Subdomain."),
        Field(name="country", dtype=types.String, description="Country."),
    ],
    source=source,
)
