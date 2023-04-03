# Standard Library
import os

# 3rd party libraries
from pydantic import BaseSettings


class TokenizerSettings(BaseSettings):
    padding: str = "max_length"
    truncation: bool = True
    add_special_tokens: bool = True
    max_length: int = (
        512  # based on sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
    )


class KeyWordTrainSettings(BaseSettings):
    """Default parameter (behaviour) for the training component of the keyword ML project."""

    # neptune ai model registry settings
    NEPTUNE_PROJECT: str = "onclusive/keywords"
    NEPTUNE_MODEL_ID: str = "KEY-KEYBERT"
    NEPTUNE_API_TOKEN: str
    # model params
    HF_MODEL_REFERENCE: str = (
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    TOKENIZER_SETTINGS: TokenizerSettings = TokenizerSettings()
    # admin
    LOCAL_OUTPUT_DIR: str = os.path.join(".", "keyword_model_artifacts")
    LOGGING_LEVEL: str = "INFO"


KEYWORD_TRAIN_SETTINGS = KeyWordTrainSettings()
