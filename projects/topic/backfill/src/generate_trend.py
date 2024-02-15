"""Trend detection."""

# Standard Library
# 3rd party libraries
from typing import Dict, List, Union

import pandas as pd
from kats.consts import TimeSeriesData
from kats.detectors.cusum_detection import CUSUMDetector
from tqdm import tqdm


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
        self, df_all_count: pd.DataFrame, all_topic_count: pd.DataFrame, topic_id: int
    ) -> bool:
        """Trend detection for single topic and keyword.

        Args:
            df_all_count (pd.DataFrame): time series dataframe for single topic and keyword
            all_topic_count (pd.DataFrame): time series dataframe for all topic
            topic_id (int): topic id
        Output:
            bool: trend or not
        """
        if df_all_count["doc_count"].sum() >= (
            0.03 * all_topic_count["doc_count"].sum()
        ):  # total number of instances of topic must be 3% of total number of documents
            # return df_all_count
            try:
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
                # tsd = TimeSeriesData(df_all_count[['time','y']])
                detector = CUSUMDetector(tsd)
                change_points = detector.detector(
                    change_directions=["increase"],
                    delta_std_ratio=2,
                    magnitude_quantile=1,
                    threshold=0.005,
                )
                if len(change_points) > 0:
                    return True
            except Exception as e:
                print("Error with topic_id: {}, {}".format(topic_id, e))
        return False

    def get_trendy(
        self,
        all_topic_count: pd.DataFrame,
        df_all_count_dict: Dict[int, pd.DataFrame],
        keyword_: str,
    ) -> List[Dict[str, Union[str, int]]]:
        """Get trend for a certain keyword.

        Args:
            df_all_count_dict (Dict[int,pd.DataFrame]): key:topic_id, value: df_all_count
            all_topic_count (pd.DataFrame): time series dataframe for all topic
            keyword_ (str): keyword
        Output:
            List of dict: information for each trendy keyword and topic
        """
        trendy_topic = []
        all_topic_count = self.remove_weekends(all_topic_count)

        for topic_id in tqdm(df_all_count_dict.keys()):
            df_all_count = df_all_count_dict[topic_id]
            if len(df_all_count) > 0:
                df_all_count = self.remove_weekends(df_all_count)
            else:
                continue

            if self.single_topic_trend(df_all_count, all_topic_count, topic_id):
                trendy_topic.append(
                    {
                        "trend_id": topic_id,
                        "trend_keyword": keyword_,
                        "trend_total_doc_count": df_all_count["doc_count"].sum(),
                    }
                )

        return trendy_topic
