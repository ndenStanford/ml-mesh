# Standard Library
import os
from typing import List, Tuple

# 3rd party libraries
from pydantic import BaseModel

# Internal libraries
from onclusiveml.tracking import TrackedModelCard, TrackedModelSpecs


# --- settings classes
class TrackedKeywordModelSpecs(TrackedModelSpecs):
    project: str = "onclusive/keywords"
    model = "KEYWORDS-BASE"


class KeywordExtractionSettings(BaseModel):
    keyphrase_ngram_range: Tuple[int, int] = (1, 1)
    stop_words: List[str] = None


class KeywordModelParams(BaseModel):
    huggingface_pipeline_task: str = "feature-extraction"
    huggingface_model_reference: str = (
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    keyword_extraction_settings: KeywordExtractionSettings = KeywordExtractionSettings()


class TrackedKeywordsBaseModelCard(TrackedModelCard):
    """Default parameter (behaviour) for the training component of the keyword ML project."""

    model_type: str = "base"
    # --- custom fields
    # model params
    model_params: KeywordModelParams = KeywordModelParams()
    # admin
    local_output_dir: str = os.path.join(".", "keyword_model_artifacts")
    logging_level: str = "INFO"
