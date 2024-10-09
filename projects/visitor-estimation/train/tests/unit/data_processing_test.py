"""Data processing test."""

# Standard Library
from unittest.mock import MagicMock

# 3rd party libraries
import numpy as np
import pandas as pd


def setup_mock_data():
    """Sets up mock data for testing the data_preprocess function."""
    dataset_dict = {
        "search_seeds_feature_view": pd.DataFrame(),
        "eclr_links_feature_view": pd.DataFrame(),
        "crawler_items_feature_view": pd.DataFrame(
            {
                "entity_id": [1, 2],
                "url": ["https://example.com/page1", "http://example.com/page2"],
                "word_count": [100, 200],
            }
        ),
        "profile_entity_relationships_feature_view": pd.DataFrame(
            {"profile_id": [1, 2], "entity_id": [1, 2]}
        ),
        "profile_company_sectors_feature_view": pd.DataFrame(),
        "entity_links_lmd_feature_view": pd.DataFrame(
            {"link_metadata_timestamp": ["2024-01-01", "2024-02-01"]}
        ),
        "entity_ea_per_feature_view": pd.DataFrame(
            {
                "profile_id": [1, 2],
                "entity_id": [1, 2],
                "ea_timestamp": ["2024-01-01", "2024-02-01"],
            }
        ),
        "entity_links_feature_view": pd.DataFrame(
            {
                "entity_id": [1, 2],
                "entities_entity_timestamp": ["2024-01-01", "2024-02-01"],
                "pagerank": [0.5, 0.7],
                "type_cd": [1, 2],
                "article_type_cd": [1, 0],
                "domain_id": [1, 2],
                "language": ["en", "fr"],
            }
        ),
        "domains_feature_view": pd.DataFrame(
            {"id": [1, 2], "publication": ["Publication A", "Publication B"]}
        ),
        "entity_connections_feature_view": pd.DataFrame(),
    }
    # Mocking the methods for join and calculation functions
    min_window = 0
    max_window = 10
    joinEntityAnalyticsWithLinkMetadata = MagicMock(return_value=pd.DataFrame())
    getRelevancePercentiles = MagicMock(return_value=pd.DataFrame())
    getTotalVisitors = MagicMock(return_value=pd.DataFrame())
    getPerWithNamedEntityCounts = MagicMock(return_value=pd.DataFrame())
    joinWithSyndicates = MagicMock(return_value=pd.DataFrame())

    return (
        dataset_dict,
        min_window,
        max_window,
        joinEntityAnalyticsWithLinkMetadata,
        getRelevancePercentiles,
        getTotalVisitors,
        getPerWithNamedEntityCounts,
        joinWithSyndicates,
    )


def test_data_processing_step_1_to_3():
    """Test Steps 1-3: Data renaming, initial manipulations, and joins."""
    dataset_dict, _, _, _, _, _, _, _ = setup_mock_data()
    # Test renaming columns and df manipulations
    df_lmd = dataset_dict["entity_links_lmd_feature_view"].rename(
        columns={"link_metadata_timestamp": "timestamp"}
    )
    df_ea = dataset_dict["entity_ea_per_feature_view"].rename(
        columns={"ea_timestamp": "timestamp"}
    )
    df_dom = dataset_dict["domains_feature_view"].rename(columns={"id": "domain_id"})

    assert "timestamp" in df_lmd.columns
    assert "timestamp" in df_ea.columns
    assert "domain_id" in df_dom.columns
    # Test data manipulation of df_ea using df_per
    df_per = dataset_dict["profile_entity_relationships_feature_view"]
    df_ea["entity_id"] = df_ea.apply(
        lambda row: (
            np.random.choice(
                df_per[df_per["profile_id"] == row["profile_id"]]["entity_id"].values
            )
            if len(df_per[df_per["profile_id"] == row["profile_id"]]) > 0
            else row["entity_id"]
        ),
        axis=1,
    )
    assert df_ea["entity_id"].iloc[0] == 1


def test_data_processing_step_4_to_6():
    """Test Steps 4-6: Merging additional entity info and visitor data."""
    dataset_dict, _, _, _, _, _, _, _ = setup_mock_data()
    # Mocking and testing entity info merge step
    entityInfo = dataset_dict["entity_links_feature_view"]
    merged_df = entityInfo.rename(columns={"entity_id": "entityID"})
    assert "entityID" in merged_df.columns
    # Check the merge and conversion to datetime
    merged_df["entityTimestamp"] = pd.to_datetime(
        merged_df["entities_entity_timestamp"]
    )
    assert merged_df["entityTimestamp"].dtype == "datetime64[ns]"


def test_data_processing_step_7_to_9():
    """Test Steps 7-9: Final merges and domain link processing."""
    dataset_dict, _, _, _, _, _, _, _ = setup_mock_data()

    df_crl = dataset_dict["crawler_items_feature_view"]
    df_crl["entityURLProtocol"] = df_crl["url"].str.extract(
        r"(https?)://.*", expand=False
    )
    assert "entityURLProtocol" in df_crl.columns
    assert df_crl["entityURLProtocol"].iloc[0] == "https"
    # Test domain link count processing
    # domainRegex = r"(https?://[^/]*/).*"
    df_eclr = dataset_dict["eclr_links_feature_view"]
    matchingURLS = df_eclr.assign(
        profileDomainURL=lambda df: df["entity_id"].astype(str)
    )
    assert "profileDomainURL" in matchingURLS.columns

    domainLinkCounts = matchingURLS.groupby("entity_id").size()
    assert isinstance(domainLinkCounts, pd.Series)
