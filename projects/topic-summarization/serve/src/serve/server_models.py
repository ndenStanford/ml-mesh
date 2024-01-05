"""Serving data models."""

# Standard Library
from typing import Dict, List

# 3rd party libraries
from pydantic import BaseModel


class PredictInputDocumentModel(BaseModel):
    """Predict input document model.

    Attributes:
        content (str): Text to generate signature for. An empty string is needed (at least)
    """

    content: List[str]


class PredictRequestModel(BaseModel):
    """Predict Request Model."""

    # configuration: PredictConfiguration
    inputs: PredictInputDocumentModel


class PredictResponseModel(BaseModel):
    """Signature response item.

    Holds the information on expected output at inference

    Attributes:
        signature (Optional[str]): Signature text in string, can be None
    """

    topic: Dict


# --- bio response models
class BioResponseModel(BaseModel):
    """Bio Response model."""

    model_name: str = "topic-detection"
