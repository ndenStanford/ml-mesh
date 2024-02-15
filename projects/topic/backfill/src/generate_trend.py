"""Trend detection."""

# 3rd party libraries
import pandas as pd
from kats.consts import TimeSeriesData
from kats.detectors.cusum_detection import CUSUMDetector


class TrendDetection:
    """Package trend detection."""

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
        self, df_all_count: pd.DataFrame, all_topic_count: pd.DataFrame
    ) -> bool:
        """Trend detection for single topic and keyword.

        Args:
            df_all_count (pd.DataFrame): time series dataframe for single topic and keyword
            all_topic_count (pd.DataFrame): time series dataframe for all topic
        Output:
            bool: trend or not
        """
        all_topic_count = self.remove_weekends(all_topic_count)
        if len(df_all_count) > 0:
            df_all_count = self.remove_weekends(df_all_count)
        else:
            return False

        if df_all_count["doc_count"].sum() >= (
            0.03 * all_topic_count["doc_count"].sum()
        ):  # total number of instances of topic must be 3% of total number of documents

            df_all_count["time"] = pd.to_datetime(df_all_count["key_as_string"])
            df_all_count = df_all_count.rename(columns={"doc_count": "y"})
            # print(df_all_count.head())

            # remove rows from all_topic_count_temp that doesn't exist in df_all_count
            # this is so we can do normalisation in correct order of rows
            all_topic_count_temp = all_topic_count[
                all_topic_count["key"].isin(df_all_count["key"])
            ]
            all_topic_count_temp = all_topic_count_temp.reset_index(drop=True)

            # normalisation
            df_all_count["predicted_topic_id_ratio"] = (
                df_all_count["y"] / all_topic_count_temp["doc_count"]
            )

            tsd = TimeSeriesData(df_all_count[["time", "predicted_topic_id_ratio"]])
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
