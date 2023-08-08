# Standard Library
from typing import Dict, List, Optional, Tuple

# 3rd party libraries
from pydantic import BaseModel


# --- prediction request models
class PredictConfiguration(BaseModel):
    """Signature request item.

    Holds the required information to be provided in the payload and their type

    Attributes:
        content (str): Text to generate signature for. An empty string is needed (at least)

        lang (Optional[str]): Text to indicate the language

        shingle_list (Optional[int])

        threshold (Optional[float])

        num_perm (Optional[int]))

        weights (Optional[Tuple[float]])
    """

    content: str
    language: Optional[str] = "en"
    shingle_list: Optional[int] = 5
    threshold: Optional[float] = 0.6
    num_perm: Optional[int] = 128
    weights: Optional[Tuple[float, float]] = (0.5, 0.5)


class PredictInputDocumentModel(BaseModel):

    document: str


class PredictRequestModel(BaseModel):

    configuration: PredictConfiguration = PredictConfiguration()
    inputs: PredictInputDocumentModel = PredictInputDocumentModel()


class PredictionExtractedSignature(BaseModel):
    """Signature response item.

    Holds the information on expected output at inference

    Attributes:
        signature (Optional[str]): Signature text in string, can be None
    """

    signature: Optional[List[str]]


class PredictResponseModel(BaseModel):

    outputs: List[PredictionExtractedSignature]


# --- bio response models
class BioResponseModel(BaseModel):

    model_name: str = "lsh-model"
    # difficult to link up all the way back to the `CompiledLshTrackedModelCard` here, so for
    # now we leave this unmodelled ith an understanding that that is what will come through in this
    # field
    model_card: Dict
