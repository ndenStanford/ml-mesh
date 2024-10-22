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
