# Standard Library
from typing import Dict, List, Tuple, Union

# 3rd party libraries
from pydantic import BaseModel


# --- prediction request models
class KeywordsPredictConfiguration(BaseModel):
    """Model class around the kwargs of the `CompiledKeyBERT`'s `extract_keywords` method. Useful if
    clients want to run different inference calls configuring
    - how many keywords should be extracted,
    - n-gram length
    - etc"""

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


class KeywordsPredictInputDocumentModel(BaseModel):

    document: str


class KeywordsPredictRequestModel(BaseModel):

    inference_configuration: KeywordsPredictConfiguration = (
        KeywordsPredictConfiguration()
    )
    inference_inputs: List[KeywordsPredictInputDocumentModel]


# --- prediction response models
class KeywordsPredictionExtractedKeyword(BaseModel):

    keyword_token: str
    keyword_score: float


class KeywordsPredictionOutputDocument(BaseModel):

    predicted_document: List[KeywordsPredictionExtractedKeyword]


class KeywordsPredictResponseModel(BaseModel):

    inference_outputs: List[KeywordsPredictionOutputDocument]


# --- bio response models
class KeywordsBioResponseModel(BaseModel):

    name: str = "keywords-model"
    # difficult to link up all the way back to the `CompiledKeywordsTrackedModelCard` here, so for
    # now we leave this unmodelled ith an understanding that that is what will come through in this
    # field
    tracked_keywords_model_card: Dict
