"""Serving data models."""

# Standard Library
from typing import Dict, List, Tuple, Union

# 3rd party libraries
from pydantic import BaseModel


# --- prediction request models
class PredictConfiguration(BaseModel):
    """Model class around the kwargs of the `CompiledKeyBERT`'s `extract_keywords` method.


    Useful if clients want to run different inference calls configuring
        - how many keywords should be extracted,
        - n-gram length
        - etc
    """

    candidates: Union[List[str], None] = None
    keyphrase_ngram_range: Tuple[int, int] = (1, 1)
    stop_words: Union[str, List[str]] = "english"
    top_n: int = 5
    min_df: int = 1
    use_maxsum: bool = False
    use_mmr: bool = False
    diversity: float = 0.5
    nr_candidates: int = 20
    seed_keywords: Union[List[str], List[List[str]], None] = None


class PredictInputDocumentModel(BaseModel):
    """Prediction input document."""

    document: str


class PredictRequestModel(BaseModel):
    """Prediction request model."""

    configuration: PredictConfiguration = PredictConfiguration()
    inputs: List[PredictInputDocumentModel]


# --- prediction response models
class PredictionExtractedKeyword(BaseModel):
    """Prediction extracted keyword."""

    keyword_token: str
    keyword_score: float


class PredictionOutputDocument(BaseModel):
    """Prediction output document."""

    predicted_document: List[PredictionExtractedKeyword]


class PredictResponseModel(BaseModel):
    """Predict response model."""

    outputs: List[PredictionOutputDocument]


# --- bio response models
class BioResponseModel(BaseModel):
    """Bio response model."""

    model_name: str = "keywords-model"
    # difficult to link up all the way back to the `CompiledKeywordsTrackedModelCard` here, so for
    # now we leave this unmodelled ith an understanding that that is what will come through in this
    # field
    model_card: Dict
