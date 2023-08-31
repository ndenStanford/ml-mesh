"""Schemas."""

# Standard Library
from typing import Optional

# Internal libraries
from onclusiveml.core.serialization import JsonApiSchema


class BioResponseModel(BaseModel):
    """Test."""


class PredictRequestModelAttributes(BaseModel):
    """Prediction request data."""

    entity_type: Optional[str] = None
    entity_text: Optional[str] = None
    text: Optional[str] = None
    score: Optional[str] = None
    sentence_index: Optional[str] = None


class PredictRequestModel(BaseModel):
    id: Optional[str] = None
    namespace: str
    data: PredictRequestModelAttributes


class PredictResponsetModelAttributes(BaseModel):
    """Prediction request data."""

    entity_type: Optional[str] = None
    entity_text: Optional[str] = None
    text: Optional[str] = None
    score: Optional[str] = None
    sentence_index: Optional[str] = None
    wiki_link: Optional[str] = None


class PredictResponseModel(BaseModel):
    ...
