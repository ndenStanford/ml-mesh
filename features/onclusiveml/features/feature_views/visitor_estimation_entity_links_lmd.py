"""Visitor Estimation Entity Links LMD."""

from datetime import timedelta

from feast import Entity, FeatureView, Field, types
from onclusiveml.features.contrib.redshift import OnclusiveRedshiftSource

# Define the entity for entity_links_lmd
entity = Entity(name="entity_links_lmd", join_keys=["entity_links_lmd_id"], description="Visitor Estimation Entity Links LMD.")

# Define the Redshift source for the feature view
source = OnclusiveRedshiftSource(
    name="visitor_estimation_entity_links_lmd",
    query="SELECT * FROM stage.stg_visitor_estimation__entity_links_metadata",
    schema="stage",
    table="stg_visitor_estimation__entity_links_metadata",
    timestamp_field="event_timestamp",
)

# Define the feature view for entity_links_lmd
feature_view = FeatureView(
    name="visitor_estimation_entity_links_lmd",
    entities=[entity],
    ttl=timedelta(days=10000),
    schema=[
        Field(name="entity_id", dtype=types.String, description="Entity ID."),
        Field(name="link_metadata_timestamp", dtype=types.String, description="Link Metadata Timestamp."),
        Field(name="fb_likes", dtype=types.String, description="Facebook Likes."),
        Field(name="fb_comments", dtype=types.String, description="Facebook Comments."),
        Field(name="fb_shares", dtype=types.String, description="Facebook Shares."),
        Field(name="fb_total", dtype=types.String, description="Facebook Total Engagement."),
        Field(name="fb_clicks", dtype=types.String, description="Facebook Clicks."),
        Field(name="twitter_retweets", dtype=types.String, description="Twitter Retweets."),
        Field(name="google_plusones", dtype=types.String, description="Google Plus Ones."),
        Field(name="linkedin_shares", dtype=types.String, description="LinkedIn Shares."),
        Field(name="twitter_favorites", dtype=types.String, description="Twitter Favorites."),
        Field(name="google_reshares", dtype=types.String, description="Google Reshares."),
        Field(name="google_replies", dtype=types.String, description="Google Replies."),
    ],
    source=source,
)
