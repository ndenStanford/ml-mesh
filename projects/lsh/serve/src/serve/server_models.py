"""Serving data models."""

# Standard Library
from typing import List, Optional

# 3rd party libraries
from pydantic import BaseModel


# --- prediction request models
class PredictConfiguration(BaseModel):
    """Signature request item.

    Holds the required information to be provided in the payload and their type

    Attributes:

        lang (Optional[str]): Text to indicate the language

        shingle_list (Optional[int])

        threshold (Optional[float])

        num_perm (Optional[int]))

    """

    language: Optional[str] = "en"
    shingle_list: Optional[int] = 5
    threshold: Optional[float] = 0.6
    num_perm: Optional[int] = 128


class PredictInputDocumentModel(BaseModel):
    """
    Attributes:

        content (str): Text to generate signature for. An empty string is needed (at least)
    """

    content: str


class PredictRequestModel(BaseModel):

    configuration: PredictConfiguration
    inputs: PredictInputDocumentModel


class PredictResponseModel(BaseModel):
    """Signature response item.

    Holds the information on expected output at inference

    Attributes:
        signature (Optional[str]): Signature text in string, can be None
    """

    signature: Optional[List[str]]


# --- bio response models
class BioResponseModel(BaseModel):

    model_name: str = "lsh-model"
