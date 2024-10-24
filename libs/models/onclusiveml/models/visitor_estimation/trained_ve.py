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
    getRelevancePercentile,
    imputeByColumns,
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
        times = pd.to_datetime(data["analyticsTimestamp"], errors="coerce")
        social = data["social"]
        metadata_times = pd.to_datetime(social["metadataTimestamp"], errors="coerce")
        # Creating a list of social metrics as in Scala code
        social_metrics = [
            social["fbLikes"],
            social["fbComments"],
            social["fbTotal"],
            social["fbShares"],
            social["linkedInShares"],
            social["googlePlusones"],
            social["twitterRetweets"],
        ]
        # Transpose and zip the times with the metrics to create metadata tuples
        md = list(zip(metadata_times, zip(*social_metrics)))
        imputed_metadata = imputeByColumns(times, md)
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
            imputed_metadata, columns=["analyticsTimestamp", "metrics"]
        )
        social_cols = [
            "fbLikes",
            "fbComments",
            "fbTotal",
            "fbShares",
            "linkedInShares",
            "googlePlusones",
            "twitterRetweets",
        ]
        for i, col in enumerate(social_cols):
            metadata_df[col] = metadata_df["metrics"].apply(lambda x: x[i])
        metadata_df.drop(columns="metrics", inplace=True)
        # Adding the additional columns to match Scala's code
        metadata_df["entityTimestamp"] = pd.Timestamp(data["entityTimestamp"])
        metadata_df["namedEntityCount"] = data["namedEntityCount"]
        metadata_df["relevancePercentile"] = getRelevancePercentile(
            self.relevance_map, data["profileID"], data["relevance"]
        )
        metadata_df["pageRank"] = data["pagerank"]
        metadata_df["company_sector_id"] = data["companySectorId"]
        metadata_df["type"] = data["typeCd"]
        metadata_df["category_id"] = data["category"]
        metadata_df["wordCount"] = data["wordCount"]
        metadata_df["domainLinkCount"] = data["domainLinkCount"]
        metadata_df["nonDomainLinkCount"] = data["nonDomainLinkCount"]
        metadata_df["isSyndicateParent"] = data["isSyndicateParent"]
        metadata_df["isSyndicateChild"] = data["isSyndicateChild"]
        # Calculating the maximum values for the social metrics
        social_maxes = (
            metadata_df[social_cols]
            .max()
            .add_suffix("Max")
            .to_frame()
            .T.reset_index(drop=True)
        )
        # Cross join the original DataFrame with the max values DataFrame
        result_df = metadata_df.merge(social_maxes, how="cross")

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