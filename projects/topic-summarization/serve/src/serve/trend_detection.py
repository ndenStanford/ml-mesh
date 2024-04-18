"""Trend detection."""

# Standard Library
from typing import Tuple, Union

import pandas as pd
from elasticsearch import Elasticsearch
from kats.consts import TimeSeriesData
from kats.detectors.cusum_detection import CUSUMDetector

# Internal libraries
from onclusiveml.data.query_profile import BaseQueryProfile, MediaAPISettings

# 3rd party libraries
from pandas import Timestamp

# Source
from src.serve.utils import (  # query_translation,
    all_profile_query,
    remove_weekends,
    topic_profile_query,
)
from src.settings import get_settings

settings = get_settings()


class TrendDetection:
    """Trend detection class used to find trend of a given profile and topic."""

    def __init__(self) -> None:
        self.es = Elasticsearch(
            [
                f"https://crawler-prod:{settings.ELASTICSEARCH_KEY.get_secret_value()}@search5-client.airpr.com"  # noqa: W505, E501
            ]
        )

    def remove_weekends(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove weekends.

        Args:
            df (pd.DataFrame): time series dataframe
        Output:
            df: pd.DataFrame
        """
        df["weekday_index"] = pd.to_datetime(df["key_as_string"]).apply(
            lambda x: x.weekday()
        )
        df = df[df["weekday_index"] <= 4]
        df = df.reset_index(drop=True)
        return df

    def single_topic_trend(
        self,
        query_profile: BaseQueryProfile,
        topic_id: str,
        start_time: pd.datetime,
        end_time: pd.datetime,
    ) -> Tuple[bool, Union[Timestamp, None]]:
        """Trend detection for single topic and keyword.

        Args:
            query_profile (BaseQueryProfile): profile to fetch query from
            topic_id (str): topic id
            start_time (pd.datetime): start time range of documents to be collected
            end_time (pd.datetime): end time range of documents to be collected
        Output:
            Tuple[bool, Union[Timestamp, None]]: bool and timestamp of inflection point
        """
        query = query_profile.es_query(MediaAPISettings())
        # Profile query
        results_all_profile_query = self.es.search(
            index=settings.es_index,
            body=all_profile_query(
                query, start_time, end_time, settings.trend_time_interval
            ),
        )["aggregations"]["daily_doc_count"]["buckets"]
        print("results_all_profile_query")
        print(results_all_profile_query)
        results_all_profile_query_no_weekends = remove_weekends(
            results_all_profile_query
        )
        df_all_topic = pd.DataFrame(results_all_profile_query_no_weekends)  # .iloc[:-1]
        print("df_all_topic")
        print(df_all_topic)
        # profile topic query
        results_topic_profile_query = self.es.search(
            index=settings.es_index,
            body=topic_profile_query(
                query, start_time, end_time, topic_id, settings.trend_time_interval
            ),
        )["aggregations"]["daily_doc_count"]["buckets"]
        print("results_topic_profile_query")
        print(results_topic_profile_query)
        if len(results_topic_profile_query) > 0:
            results_topic_profile_query_no_weekends = remove_weekends(
                results_topic_profile_query
            )
            df_single_topic = pd.DataFrame(
                results_topic_profile_query_no_weekends
            )  # .iloc[:-1]
            print("df_single_topic")
            print(df_single_topic)
        else:
            return False, None

        print("here1")
        print(df_single_topic["doc_count"].sum())
        print("here2")
        print(settings.TOPIC_DOCUMENT_THRESHOLD)
        print(settings.TOPIC_DOCUMENT_THRESHOLD * df_all_topic["doc_count"].sum())

        if df_single_topic["doc_count"].sum() >= (
            settings.TOPIC_DOCUMENT_THRESHOLD * df_all_topic["doc_count"].sum()
        ):
            # total number of instances of topic must be 3% of total number of documents
            df_single_topic["time"] = pd.to_datetime(df_single_topic["key_as_string"])
            df_single_topic = df_single_topic.rename(columns={"doc_count": "y"})
            # remove rows from all_topic_count_temp that doesn't exist in df_all_count
            # this is so we can do normalisation in correct order of rows
            df_all_topic_temp = df_all_topic[
                df_all_topic["key"].isin(df_single_topic["key"])
            ]
            df_all_topic_temp = df_all_topic_temp.reset_index(drop=True)
            # normalisation
            df_single_topic["predicted_topic_id_ratio"] = (
                df_single_topic["y"] / df_all_topic_temp["doc_count"]
            )

            tsd = TimeSeriesData(df_single_topic[["time", "predicted_topic_id_ratio"]])
            detector = CUSUMDetector(tsd)
            change_points = detector.detector(
                change_directions=["increase"],
                delta_std_ratio=2,
                magnitude_quantile=1,
                threshold=0.005,
            )
            if len(change_points) > 0:
                return True, change_points[0].start_time
        return False, None
