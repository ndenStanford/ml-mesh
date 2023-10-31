"""Serving data models."""

# Standard Library
from typing import Dict, List, Optional

# 3rd party libraries
from pydantic import BaseModel


# --- prediction request models
class PredictConfiguration(BaseModel):
    """GPT parameters.

    Holds the required information to be provided in the payload and their type
    """

    content: List[str] = [""]  # industry for first, article for second
    industry: str = ""
    max_tokens: Optional[int] = 0
    temperature: Optional[float] = 1
    top_p: Optional[float] = 1
    presence_penalty: Optional[float] = 0
    frequency_penalty: Optional[float] = 0
    model: Optional[str] = "gpt-4"


class PredictInputDocumentModel(BaseModel):
    """Predict input document model.

    Attributes:
        content (str): Text to generate signature for. An empty string is needed (at least)
    """

    industry: str
    content: List[str]


class PredictRequestModel(BaseModel):
    """Predict Request Model."""

    configuration: PredictConfiguration
    inputs: PredictInputDocumentModel


class PredictResponseModel(BaseModel):
    """Signature response item.

    Holds the information on expected output at inference

    Attributes:
        signature (Optional[str]): Signature text in string, can be None
    """

    # signature: Optional[List[str]]
    topic: Dict


# --- bio response models
class BioResponseModel(BaseModel):
    """Bio Response model."""

    model_name: str = "topic-detection"
