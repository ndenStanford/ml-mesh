# isort: skip_file
"""Impact quantification."""

# Standard Library
from datetime import datetime
from typing import Dict

# 3rd party libraries
import numpy as np
import pandas as pd
import pymannkendall as mk
from elasticsearch import Elasticsearch
from numpy.typing import ArrayLike
from prophet import Prophet

# Internal libraries
from onclusiveml.queries.query_profile import BaseQueryProfile, MediaAPISettings
from onclusiveml.serving.serialization.topic_summarization.v1 import (
    ImpactCategoryLabel,
)

# Source
from src.serve.utils import (
    all_global_query,
    all_profile_boolean_query,
    remove_weekends,
    topic_global_query,
    topic_profile_query,
)
import src.settings
from src.settings import get_settings

src.settings.get_settings_clear_cache()


class ImpactQuantification:
    """Package trend detection."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self.es = Elasticsearch(
            [
                f"https://crawler-prod:{self.settings.ELASTICSEARCH_KEY.get_secret_value()}@search5-client.airpr.com"  # noqa: W505, E501
            ],
            timeout=self.settings.ES_TIMEOUT,
        )

    def decompose_trend(self, series_profile: ArrayLike) -> ArrayLike:
        """Decomposes trend component of a given time series profile using prophet.

        Args:
            series_profile (ArrayLike): time series queried from GCH
        Output:
            series_profile_trend (ArrayLike): time series trend from decomposition
        """
        df = pd.DataFrame()
        df["ds"] = pd.date_range(start="1/1/2018", periods=len(series_profile))
        df["y"] = series_profile

        m = Prophet()
        m.fit(df)
        component = m.predict(df)
        series_profile_trend = component["trend"].values
        return series_profile_trend

    def insert_into_sorted_list(self, sorted_list: Dict, new_keys: Dict) -> Dict:
        """Time-series helper function."""
        result = sorted_list[:]
        for i in new_keys:
            index = 0
            while index < len(result) and result[index]["key"] < i["key"]:
                index += 1
            # Check if the key already exists in the list
            if index < len(result) and result[index]["key"] == i["key"]:
                continue

            result.insert(
                index,
                {"key": i["key"], "doc_count": 0, "key_as_string": i["key_as_string"]},
            )
        return result

    def trend(self, query_profile: BaseQueryProfile, topic_id: int) -> Dict:
        """Analysis of time series of document counts.

        Args:
            query_profile (BaseQueryProfile): profile to fetch query from
            topic_id (int): topic id
        Output:
            result (Dict): result of trend analysis
        """
        query = query_profile.es_query(MediaAPISettings())

        end_time = pd.Timestamp(datetime.now())
        start_time = end_time - pd.Timedelta(days=self.settings.impact_lookback_days)
        # ========== Profile (global) ==========
        # Global count of all documents from ES
        series_global_es = self.es.search(
            index=self.settings.es_index,
            body=all_global_query(start_time, end_time, self.settings.time_interval),
        )["aggregations"]["daily_doc_count"]["buckets"]
        # Remove weekends
        series_global_es = remove_weekends(series_global_es)
        # Global count of all documents of a topic from ES
        series_topic_es = self.es.search(
            index=self.settings.es_index,
            body=topic_global_query(
                start_time, end_time, topic_id, self.settings.time_interval
            ),
        )["aggregations"]["daily_doc_count"]["buckets"]
        # Remove weekends
        series_topic_es = remove_weekends(series_topic_es)
        # if there is mismatch between both queries, add unique elements from global to topic
        if len(series_global_es) != len(series_topic_es):
            # Extract the keys from series_topic_es
            topic_keys = {d["key"] for d in series_topic_es}
            # Iterate over global and add missing keys to topic
            for d in series_global_es:
                if d["key"] not in topic_keys:
                    series_topic_es.append(
                        {
                            "key_as_string": d["key_as_string"],
                            "key": d["key"],
                            "doc_count": 0,
                            "weekday_index": d["weekday_index"],
                        }
                    )
            # Sort series_topic_es by the "key"
            series_topic_es = sorted(series_topic_es, key=lambda d: d["key"])
        series_topic = np.array([i["doc_count"] for i in series_topic_es])
        series_global = np.array([i["doc_count"] for i in series_global_es])
        # calculate global ratio
        global_ratio = series_topic / series_global
        # Decomposes trend
        series_global_trend = self.decompose_trend(series_global)
        series_topic_trend = self.decompose_trend(series_topic)
        # calculate ratio of trend between topic and global series
        global_trend_ratio = series_topic_trend / series_global_trend
        # ========== Profile (local) ==========
        # Profile count from ES
        series_profile_es = self.es.search(
            index=self.settings.es_index,
            body=all_profile_boolean_query(
                query, start_time, end_time, self.settings.time_interval
            ),
        )["aggregations"]["daily_doc_count"]["buckets"]
        # Remove weekends
        series_profile_es = remove_weekends(series_profile_es)
        series_profile = np.array([i["doc_count"] for i in series_profile_es])
        # Profile count of a topic from ES
        series_topic_profile_es = self.es.search(
            index=self.settings.es_index,
            body=topic_profile_query(
                query, start_time, end_time, topic_id, self.settings.time_interval
            ),
        )["aggregations"]["daily_doc_count"]["buckets"]
        # Remove weekends
        series_topic_profile_es = remove_weekends(series_topic_profile_es)
        series_topic_profile_es = self.insert_into_sorted_list(
            series_topic_profile_es, series_profile_es
        )
        series_topic_profile = np.array(
            [i["doc_count"] for i in series_topic_profile_es]
        )
        # Calculate local ratio
        local_ratio = series_topic_profile / series_profile
        # Decompose trend
        series_profile_trend = self.decompose_trend(series_profile)
        series_topic_profile_trend = self.decompose_trend(series_topic_profile)
        # Calculate ratio of trend between topic profile and profile series
        local_trend_ratio = series_topic_profile_trend / series_profile_trend

        num_points = len(local_ratio)
        const = 0.01
        weight = np.exp(np.arange(num_points) * const) / np.exp(0 * const)
        # Calculate ratios
        weighted_local_ratio = np.nansum(weight * local_ratio) / np.nansum(weight)
        weighted_global_ratio = np.nansum(weight * global_ratio) / np.nansum(weight)

        result = dict()
        result["weighted_local_ratio"] = weighted_local_ratio
        result["weighted_global_ratio"] = weighted_global_ratio
        result["local_trend_ratio"] = local_trend_ratio
        result["global_trend_ratio"] = global_trend_ratio
        return result

    def quantify_impact(self, query_profile: BaseQueryProfile, topic_id: int) -> str:
        """Quntify impact of detected trends.

        Args:
            query_profile (BaseQueryProfile): profile to fetch query from
            topic_id (int): topic id
        Output:
            impact (str): impact level (low, mid, high)
        """
        self.result = self.trend(query_profile, topic_id)
        raw_baseline_bool = (
            self.result["weighted_local_ratio"] > self.settings.local_raio_cutoff
        )
        global_vs_local_bool = (
            self.result["weighted_local_ratio"] / self.result["weighted_global_ratio"]
            > self.settings.global_local_comparison_ratio_cutoff
        )

        ts = self.result["local_trend_ratio"]
        mk_result = mk.original_test(ts)
        mk_test_bool = mk_result.Tau > self.settings.mf_tau_cutoff

        if (not raw_baseline_bool) or (not global_vs_local_bool) or (not mk_test_bool):
            return ImpactCategoryLabel.LOW
        elif (raw_baseline_bool) and (global_vs_local_bool) and (mk_test_bool):
            return ImpactCategoryLabel.MID
        else:
            return ImpactCategoryLabel.HIGH
