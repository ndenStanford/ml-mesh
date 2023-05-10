# Standard Library
import os
from typing import List, Tuple

# Internal libraries
from onclusiveml.tracking import (
    TrackedModelCard,
    TrackedModelSpecs,
    TrackedParams,
)


# --- settings classes
class TrackedKeywordModelSpecs(TrackedModelSpecs):
    project: str = "onclusive/keywords"
    model = "KEYWORDS-TRAINED"

    class Config:
        env_file = "src/config/.dev", "src/config/.prod"
        env_file_encoding = "utf-8"


class Inputs(TrackedParams):

    sample_documents: List[str] = []

    class Config:
        env_file = "src/config/.dev", "src/config/.prod"
        env_file_encoding = "utf-8"


class KeywordExtractionSettings(TrackedParams):
    keyphrase_ngram_range: Tuple[int, int] = (1, 1)
    stop_words: List[str] = None
    top_n: int = 3

    class Config:
        env_file = "src/config/.dev", "src/config/.prod"
        env_file_encoding = "utf-8"


class KeywordModelParams(TrackedParams):
    huggingface_pipeline_task: str = "feature-extraction"
    huggingface_model_reference: str = (
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    keyword_extraction_settings: KeywordExtractionSettings = KeywordExtractionSettings()

    class Config:
        env_file = "src/config/.dev", "src/config/.prod"
        env_file_encoding = "utf-8"


class TrackedKeywordsBaseModelCard(TrackedModelCard):
    """The model card for the base model of the keywords ML project."""

    model_type: str = "trained"
    # --- custom fields
    # model params
    model_params: KeywordModelParams = KeywordModelParams()
    model_inputs: Inputs = Inputs()
    # admin
    local_output_dir: str = os.path.join(".", "keyword_model_artifacts")
    logging_level: str = "INFO"

    class Config:
        env_file = "src/config/.dev", "src/config/.prod"
        env_file_encoding = "utf-8"
