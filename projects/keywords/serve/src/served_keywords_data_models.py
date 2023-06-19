# Standard Library
from typing import Dict, List

# 3rd party libraries
from pydantic import BaseModel

# Internal libraries
from onclusiveml.serving.rest.serve import (
    ProtocolV1RequestModel,
    ProtocolV1ResponseModel,
)


# --- prediction request models
class KeywordsPredictInputDocumentModel(BaseModel):

    document: str


class KeywordsPredictRequestModel(ProtocolV1RequestModel):

    instances: List[KeywordsPredictInputDocumentModel]


# --- prediction response models
class KeywordsPredictionExtractedKeyword(BaseModel):

    keyword_token: str
    keyword_score: float


class KeywordsPredictionOutputDocument(BaseModel):

    predicted_document: List[KeywordsPredictionExtractedKeyword]


class KeywordsPredictResponseModel(ProtocolV1ResponseModel):

    predictions: List[KeywordsPredictionOutputDocument]


# --- bio response models
class KeywordsBioResponseModel(BaseModel):

    name: str = "keywords-model"
    # difficult to link up all the way back to the `CompiledKeywordsTrackedModelCard` here, so for
    # now we leave this unmodelled ith an understanding that that is what will come through in this
    # field
    tracked_keywords_model_card: Dict
