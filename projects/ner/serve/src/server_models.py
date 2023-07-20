# Standard Library
from typing import Dict, List, Optional

# 3rd party libraries
from pydantic import BaseModel


# --- prediction request models
class PredictConfiguration(BaseModel):

    return_pos: Optional[bool] = True


class PredictInputContentModel(BaseModel):

    content: str


class PredictRequestModel(BaseModel):

    configuration: PredictConfiguration = PredictConfiguration()
    inputs: PredictInputContentModel


# --- prediction response models
class PredictionExtractedEntity(BaseModel):

    entity_type: str
    entity_text: str
    score: float
    sentence_index: int
    start: Optional[int] = None
    end: Optional[int] = None


class PredictionOutputContent(BaseModel):

    predicted_content: List[PredictionExtractedEntity]


class PredictResponseModel(BaseModel):

    outputs: PredictionOutputContent


# --- bio response models
class BioResponseModel(BaseModel):

    model_name: str = "ner-model"
    model_card: Dict
