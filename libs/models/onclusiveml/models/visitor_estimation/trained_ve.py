"""Trained VE."""

# Standard Library
import os
import pickle
from pathlib import Path
from typing import List, Union

# 3rd party libraries
import numpy as np
import pandas as pd

# Internal libraries
from onclusiveml.core.logging import get_default_logger
from onclusiveml.models.visitor_estimation.utils import (
    convert_df_columns_to_camel,
    get_relevance_percentile,
    impute_by_columns,
)


logger = get_default_logger(__name__, level=20)


class TrainedVE:
    """Class for using trained visitor estimation model."""

    def __init__(self, trained_ve_pipeline, relevance_map):
        self.trained_ve_pipeline = trained_ve_pipeline
        self.relevance_map = relevance_map

    @classmethod
    def from_pretrained(cls, directory: Union[str, Path]) -> "TrainedVE":
        """Load the trained visitor estimation pipeline from a specified directory.

        Args:
            directory (Union[str, Path]): The path to the file where the trained model pipeline is stored.

        Returns:
            TrainedVE: The loaded trained VE object
        """
        model_path = os.path.join(directory, "trained_pipeline")
        with open(model_path, "rb") as f:
            trained_ve_pipeline = pickle.load(f)

        relevance_map_path = os.path.join(directory, "relevancemap.pkl")
        with open(relevance_map_path, "rb") as f:
            relevance_map = pickle.load(f)

        logger.info(f"Trained pipeline and relevance map loaded from {directory}")
        return cls(trained_ve_pipeline=trained_ve_pipeline, relevance_map=relevance_map)

    def preprocess(self, data: dict) -> pd.DataFrame:
        """Preprocess the input data to prepare it for the visitor estimation model.

        Args:
            data (dict): The raw input data in JSON format containing analytics, social, and metadata information.

        Returns:
            pd.DataFrame: The processed data, ready for prediction with the model.
        """
        missing_placeholder = -1
        times = pd.to_datetime(data["analytics_timestamp"], errors="coerce")
        social = data["social"]
        metadata_times = pd.to_datetime(social["metadata_timestamp"], errors="coerce")
        # Creating a list of social metrics as in Scala code
        social_metrics = [
            social["fb_likes"],
            social["fb_comments"],
            social["fb_total"],
            social["fb_shares"],
            social["linkedIn_shares"],
            social["google_plusones"],
            social["twitter_retweets"],
        ]
        # Transpose and zip the times with the metrics to create metadata tuples
        md = list(zip(metadata_times, zip(*social_metrics)))
        imputed_metadata = impute_by_columns(times, md)
        imputed_metadata = [
            (
                date,
                [
                    value if value is not None else missing_placeholder
                    for value in values
                ],
            )
            for date, values in imputed_metadata
        ]
        # Converting the imputed metadata into a DataFrame
        metadata_df = pd.DataFrame(
            imputed_metadata, columns=["analytics_timestamp", "metrics"]
        )
        social_cols = [
            "fb_likes",
            "fb_comments",
            "fb_total",
            "fb_shares",
            "linkedIn_shares",
            "google_plusones",
            "twitter_retweets",
        ]
        for i, col in enumerate(social_cols):
            metadata_df[col] = metadata_df["metrics"].apply(lambda x: x[i])
        metadata_df.drop(columns="metrics", inplace=True)
        # Adding the additional columns to match Scala's code
        metadata_df = metadata_df.assign(
            entity_timestamp=pd.Timestamp(data["entity_timestamp"]),
            named_entity_count=data["named_entity_count"],
            relevance_percentile=get_relevance_percentile(
                self.relevance_map, data["profile_id"], data["relevance"]
            ),
            page_rank=data["page_rank"],
            company_sector_id=data["company_sector_id"],
            type=data["type_cd"],
            category_id=data["category"],
            word_count=data["word_count"],
            domain_link_count=data["domain_link_count"],
            non_domain_link_count=data["non_domain_link_count"],
            is_syndicate_parent=data["is_syndicate_parent"],
            is_syndicate_child=data["is_syndicate_child"],
        )
        # Calculating the maximum values for the social metrics
        social_maxes = (
            metadata_df[social_cols]
            .max()
            .add_suffix("_max")
            .to_frame()
            .T.reset_index(drop=True)
        )
        # Cross join the original DataFrame with the max values DataFrame
        result_df = metadata_df.merge(social_maxes, how="cross")
        result_df = convert_df_columns_to_camel(
            result_df, excluded_columns=["company_sector_id", "category_id"]
        )

        return result_df

    def inference(self, df: pd.DataFrame) -> List[float]:
        """Perform inference using the trained visitor estimation model.

        Args:
            model: The trained model pipeline.
            df (pd.DataFrame): The preprocessed input data.

        Returns:
            List[float]: The predicted visitor counts.
        """
        model = self.trained_ve_pipeline
        X_preprocessed = model.named_steps["data_pipe"].transform(df)
        predictions = model.named_steps["model"].predict(X_preprocessed)
        # Step 2: Apply the UnlogTransformer to transform the predictions
        result = df.copy()
        result["logPredictions"] = predictions
        result["predictedVisitors"] = np.expm1(result["logPredictions"] * np.log(2))
        # Step 3: Return the unlogged predictions
        return result["predictedVisitors"].tolist()

    def __call__(self, input: List[dict]) -> List[float]:
        """Run the full visitor estimation process on the input data.

        Args:
            input (List[dict]): The raw input data in JSON format for which to estimate visitors.

        Returns:
            List[float]: A list of predicted visitor counts.
        """
        df = self.preprocess(input[0])
        predicted_visitors = self.inference(df)
        return predicted_visitors
