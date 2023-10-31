"""Serving data models."""

# Standard Library
from typing import List, Optional

# 3rd party libraries
from pydantic import BaseModel


# --- prediction request models
class PredictNamespace(BaseModel):
    """namespace.

    Holds the name of the api

    Attributes:
        content (str): lsh
    """

    namespace: str = "lsh"


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
    """Predict input document model.

    Attributes:
        content (str): Text to generate signature for. An empty string is needed (at least)
    """

    content: str


class PredictDataModel(BaseModel):
    """Predict data Model."""

    namespace: PredictNamespace
    attributes: PredictInputDocumentModel
    parameters: PredictConfiguration


class PredictRequestModel(BaseModel):
    """Predict Request Model."""

    data: PredictDataModel


class PredictSignatureModel(BaseModel):
    """Signature response item.

    Holds the information on expected output at inference

    Attributes:
        signature (Optional[str]): Signature text in string, can be None
    """

    signature: Optional[List[str]]


class PredictIdentifierResponse(BaseModel):
    """identifier.

    Holds the name of the identifier

    Attributes:
        content (Optional[str]): None
    """

    identifier: Optional[str] = None


class PredictDataModelResponse(BaseModel):
    """dataresponse item.

    Holds the information on expected data output in the json format

    Attributes:
        indentifier: (Optional[str]): identifier text in string, can be None
        namespace: (str): name of the model
        signature (Optional[str]): Signature text in string, can be None
    """

    identifier: PredictIdentifierResponse
    namespace: PredictNamespace
    attributes: PredictSignatureModel


class PredictVersion(BaseModel):
    """Version.

    Holds the version number
    Attributes:
        int: version number
    """

    version: int = 1


class PredictResponseModel(BaseModel):
    """Predict Response Model."""

    version: PredictVersion
    data: PredictDataModelResponse


# --- bio response models
class BioResponseModel(BaseModel):
    """Bio Response model."""

    model_name: str = "lsh"
