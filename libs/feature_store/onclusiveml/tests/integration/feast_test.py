"""Feast feature store test."""

# Internal libraries
from onclusiveml.feature_store.feast import FeastFeatureStore


def test_get_historical_features_ve(settings, entity_df_ve):
    """Test get historical features."""
    fs = FeastFeatureStore.from_settings(settings)

    dataset = fs.get_historical_features(
        entity_df=entity_df_ve,
        features=[
            "visitor_estimation_crawler_items:entity_id",
            "visitor_estimation_crawler_items:word_count",
            "visitor_estimation_crawler_items:extracted_entities",
            "visitor_estimation_crawler_items:url",
        ],
    )

    assert len(dataset) > 0
    assert set(["entity_id", "word_count", "extracted_entities", "url"]) <= set(
        dataset.columns
    )


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

    assert len(dataset) > 0
    assert set(["topic_1", "content", "title"]) <= set(dataset.columns)


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

    assert len(dataset) > 0
    assert set(["topic_1", "content", "title", "topic_1_llm"]) <= set(dataset.columns)


def test_get_training_dataset(settings):
    """Test get full dataset."""
    fs = FeastFeatureStore.from_settings(settings)

    dataset = fs.get_training_dataset(
        name="iptc_first_level",
        join_key_columns=[],
        feature_name_columns=["topic_1", "content", "language"],
        timestamp_field="created_at",
    )

    assert len(dataset) > 0
    assert set(["topic_1", "content", "language"]) <= set(dataset.columns)
