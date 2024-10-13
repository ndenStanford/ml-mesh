"""Feast feature store test."""

# Internal libraries
from onclusiveml.feature_store.feast import FeastFeatureStore


def test_get_historical_features(settings, entity_df):
    """Test get historical features."""
    fs = FeastFeatureStore.from_settings(settings)

    dataset = fs.get_historical_features(
        entity_df=entity_df,
        features=[
            "iptc_first_level:topic_1",
            "iptc_first_level:content",
            "iptc_first_level:title",
        ],
    )

    print(dataset)
    print(dataset.iloc[0])


def test_get_historical_features_on_demand(settings, entity_df):
    """Test get historical features."""
    fs = FeastFeatureStore.from_settings(settings)

    dataset = fs.get_historical_features(
        entity_df=entity_df,
        features=[
            "iptc_first_level:topic_1",
            "iptc_first_level:content",
            "iptc_first_level:title",
            "iptc_first_level_on_demand_feature_view:topic_1_llm",
        ],
    )

    print(dataset)
    print(dataset.iloc[0])


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
    print(dataset.iloc[0])
