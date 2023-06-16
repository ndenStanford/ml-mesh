# Standard Library
from pathlib import Path
from typing import Union

# 3rd party libraries
from pydantic import BaseSettings

# Internal libraries
from onclusiveml.serving.rest import ServingParams


class KeywordsServedModelParams(BaseSettings):

    model_artifact_directory: Union[str, Path] = "src/keywords_model_artifacts"
    document_pipeline_artifact: Union[str, Path] = "compiled_document_pipeline"
    word_pipeline_artifact: Union[str, Path] = "compiled_word_pipeline"
    model_card: str = "model_card.json"


class KeywordsServingParams(ServingParams):

    pass
