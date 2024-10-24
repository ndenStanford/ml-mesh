"""Conftest."""

# 3rd party libraries
import pandas as pd
import pytest

# Internal libraries
from onclusiveml.feature_store.settings import FeastFeatureStoreSettings


@pytest.fixture
def settings() -> FeastFeatureStoreSettings:
    """Feast settings."""
    return FeastFeatureStoreSettings()


@pytest.fixture
def entity_df() -> pd.DataFrame:
    """Entity df."""
    return """SELECT iptc_id, CURRENT_TIMESTAMP AS event_timestamp FROM "features"."pred_iptc_first_level"
LIMIT 10"""


@pytest.fixture
def entity_df_ve() -> pd.DataFrame:
    """Entity df."""
    return """SELECT crawler_items_id, CURRENT_TIMESTAMP AS event_timestamp FROM "stage"."stg_visitor_estimation__crawler_items"
LIMIT 10"""
