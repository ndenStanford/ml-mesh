"""Feast feature store test."""

# Internal libraries
from onclusiveml.feature_store.feast import FeastFeatureStore


def test_get_historical_features(settings, entity_df):
    """Test get historical features."""
    fs = FeastFeatureStore.from_settings(settings)

    fs.get_historical_features(
        entity_df=entity_df,
        features=["iptc_first_level:topic_1", "iptc_first_level:content"],
    )


def test_get_training_dataset(settings):
    """Test get full dataset."""
    fs = FeastFeatureStore.from_settings(settings)

    dataset = fs.get_training_dataset(
        name="iptc_first_level",
        join_key_columns=[],
        feature_name_columns=["topic_1", "content", "language"],
        timestamp_field="created_at",
    )

    print(dataset)
