"""Trend detection."""

# Standard Library
from typing import Any

# 3rd party libraries
import pandas as pd
from kats.consts import TimeSeriesData
from kats.detectors.cusum_detection import CUSUMDetector


class TrendDetection:
    """Package trend detection."""

    def convert_to_dataframe(self, time_series: Any) -> pd.DataFrame:
        """Convert timeseries list of dicts into dataframes.

        Args:
            time_series (Any): time series
        Output:
            pd.DataFrame: time series in dataframe format
        """
        return pd.DataFrame(time_series)

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

    def single_topic_trend(self, time_series_topic: Any, time_series_all: Any) -> bool:
        """Trend detection for single topic and keyword.

        Args:
            time_series_topic (Any): time series for single topic and keyword
            time_series_all (Any): time series for all topic
        Output:
            bool: trend or not
        """
        df_single_topic = self.convert_to_dataframe(time_series_topic)
        df_all_topic = self.convert_to_dataframe(time_series_all)

        df_all_topic = self.remove_weekends(df_all_topic)
        if len(df_single_topic) > 0:
            df_single_topic = self.remove_weekends(df_single_topic)
        else:
            return False

        if df_single_topic["doc_count"].sum() >= (
            0.03 * df_all_topic["doc_count"].sum()
        ):  # total number of instances of topic must be 3% of total number of documents

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
                return True
        return False
