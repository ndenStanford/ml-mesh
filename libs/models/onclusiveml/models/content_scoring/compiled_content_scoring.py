"""Compile Content Scoring model."""

# Standard Library
from pathlib import Path
from typing import Any, Dict, List, Union

# ML libs
import torch

# 3rd party libraries
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OrdinalEncoder

# Internal libraries
from onclusiveml.core.logging import get_default_logger


logger = get_default_logger(__name__, level=20)


class CompiledContentScoring:
    """Class for performing content scoring using a trained model."""

    def __init__(
        self,
        trained_content_model: RandomForestClassifier,
    ):
        self.trained_content_model = trained_content_model

    @classmethod
    def from_pretrained(
        cls, content_model_directory: Union[Path, str]
    ) -> "CompiledContentScoring":
        """Load CompiledContentScoring object from specified directory.

        Args:
            content_model_directory (Union[Path, str]): The directory path containing the trained
                content scoring model.

        Returns:
            CompiledContentScoring: The loaded compiled content scoring object.
        """
        trained_content_model = torch.load(content_model_directory)

        return cls(trained_content_model=trained_content_model)

    def preprocess_data(self, data: Dict) -> pd.DataFrame:
        """Preprocess the input Dictionary.

        Args:
            df (dict): Input dict containing data to be preprocessed.

        Returns:
            pd.DataFrame: Preprocessed DataFrame.
        """
        df = pd.DataFrame(data)
        numerical_cols = ["pagerank", "reach", "score"]
        categorical_cols = [
            "lang",
            "media_type",
            "label",
            "publication",
            "country",
            "is_copyrighted",
            "type_of_summary",
        ]
        X = df[numerical_cols + categorical_cols]
        ordinal_encoder = OrdinalEncoder()
        # Encode categorical features
        X[categorical_cols] = ordinal_encoder.fit_transform(X[categorical_cols])

        return X

    def postprocess_predictions(self, predictions: List[Any]) -> List[Any]:
        """Post-process the predictions.

        Args:
            Tuple: Predictions

        Returns:
            Tuple: associated output
        """
        labels = ["rejected", "accepted"]
        processed_predictions = [labels[prediction] for prediction in predictions]
        return processed_predictions

    def inference(self, X: pd.DataFrame) -> List[Any]:
        """Perform inference on the input data.

        Args:
            X (pd.DataFrame): Input DataFrame containing features for prediction.

        Returns:
            Tuple: Predicted content messages.
        """
        content_messages = self.trained_content_model.predict(X)
        processed_content_messages = self.postprocess_predictions(content_messages)

        return processed_content_messages

    def __call__(self, df: Dict) -> Dict[str, List[Any]]:
        """Perform content scoring on input data.

        Args:
            df (Dict): Input dictionary containing features for prediction.

        Returns:
            Tuple: Predicted content messages.
        """
        preprocessed_df = self.preprocess_data(df)
        content_messages = self.inference(preprocessed_df)
        return {"boolean_messages": content_messages}
