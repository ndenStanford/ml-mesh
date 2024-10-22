"""Base feature store."""

# Standard Library
import datetime
from abc import abstractmethod
from typing import List, Union

# 3rd party libraries
import pandas as pd

# Internal libraries
from onclusiveml.core.base import FromSettings


class BaseFeatureStore(FromSettings):
    """Feature store base class."""

    @abstractmethod
    def get_historical_features(
        self,
        entity_df: Union[pd.DataFrame, str],
        features: List[str],
        full_feature_names: bool = False,
    ) -> pd.DataFrame:
        """Returns the historical features for batch scoring.

        Args:
            entity_df: The entity DataFrame or entity name.
            features: The features to retrieve.
            full_feature_names: Whether to return the full feature names.

        Returns:
            The historical features as a Pandas DataFrame.
        """

    @abstractmethod
    def get_training_dataset(
        self,
        join_key_columns: List[str],
        feature_name_columns: List[str],
        timestamp_field: str,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
    ) -> pd.DataFrame:
        """Returns the full dataset for training.

        Args:
            join_key_columns: The columns of the join keys.
            feature_name_columns: The columns of the features.
            timestamp_field: The timestamp column.
            start_date: The start of the time range.
            end_date: The end of the time range.

        Returns:
            The full dataset as a Pandas DataFrame.
        """
