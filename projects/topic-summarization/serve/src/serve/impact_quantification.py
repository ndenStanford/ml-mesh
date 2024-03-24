"""Impact quantification."""
from typing import Dict, List

import numpy as np
import pandas as pd
from elasticsearch import Elasticsearch
from prophet import Prophet

from src.serve.utils import (
    all_global_query,
    all_profile_boolean_query,
    query_translation,
    topic_global_query,
    topic_profile_query,
)
from src.settings import get_settings

settings = get_settings()


class ImpactQuantification:
    """Package trend detection."""

    def __init__(self) -> None:
        self.es = Elasticsearch(
            [
                f"https://crawler-prod:{settings.ELASTICSEARCH_KEY.get_secret_value()} \
                    @search5-client.airpr.com"
            ]
        )

    def decompose_trend(self, series_profile: List[float]) -> np.array:
        """Decomposes trend component of a given time series profile using prophet.

        Args:
            series_profile (List[float]): time series queried from GCH
        Output:
            series_profile_trend (List[float]): time series trend from decomposition
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

    def remove_weekends(self, results: Dict) -> Dict:
        """Time-series helper function."""
        df = pd.DataFrame(results)
        # remove weekends
        df["weekday_index"] = pd.to_datetime(df["key_as_string"]).apply(
            lambda x: x.weekday()
        )
        df = df[df["weekday_index"] <= 4]
        return df.to_dict("records")

    def trend(self, boolean_query: str, topic_id: int) -> Dict:
        """Analysis of time series of document counts.

        Args:
            boolean_query (str): boolean query of a profile
            topic_id (int): topic id
        Output:
            result (Dict): result of trend analysis
        """
        query = query_translation(boolean_query)
        end_time = pd.Timestamp.now()
        start_time = end_time - pd.Timedelta(days=settings.lookback_days)

        # ========== Profile (global) ==========
        # Global count of all documents from ES
        series_global_es = self.es.search(
            index=settings.es_index,
            body=all_global_query(start_time, end_time, settings.time_interval),
        )["aggregations"]["daily_doc_count"]["buckets"]
        # Remove weekends
        # series_global_es = remove_weekends(series_global_es)
        series_global = np.array([i["doc_count"] for i in series_global_es])

        # Global count of all documents of a topic  from ES
        series_topic_es = self.es.search(
            index=settings.es_index,
            body=topic_global_query(
                start_time, end_time, topic_id, settings.time_interval
            ),
        )["aggregations"]["daily_doc_count"]["buckets"]
        # Remove weekends
        # series_topic_es = remove_weekends(series_topic_es)
        series_topic = np.array([i["doc_count"] for i in series_topic_es])

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
            index=settings.es_index,
            body=all_profile_boolean_query(
                query, start_time, end_time, settings.time_interval
            ),
        )["aggregations"]["daily_doc_count"]["buckets"]

        # Remove weekends
        # series_profile_es = remove_weekends(series_profile_es)
        series_profile = np.array([i["doc_count"] for i in series_profile_es])

        # Profile count of a topic from ES
        series_topic_profile_es = self.es.search(
            index=settings.es_index,
            body=topic_profile_query(
                query, start_time, end_time, topic_id, settings.time_interval
            ),
        )["aggregations"]["daily_doc_count"]["buckets"]

        # Remove weekends
        # series_topic_profile_es = remove_weekends(series_topic_profile_es)
        series_topic_profile_es = self.insert_into_sorted_list(
            series_topic_profile_es, series_profile_es
        )
        series_topic_profile = np.array(
            [i["doc_count"] for i in series_topic_profile_es]
        )
        print("Topic Profile Count:", series_topic_profile)

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


# query = '("Apple Music" OR AppleMusic) AND sourcecountry:[ESP,AND] AND sourcetype:print'
# topic_id = 436

# impact_quantifier = ImpactQuantification()
# result = impact_quantifier.trend(query, topic_id)
# print(result)
