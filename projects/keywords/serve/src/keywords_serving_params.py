# Standard Library
from pathlib import Path
from typing import Union

# Internal libraries
from onclusiveml.serving.rest import ServingParams


class KeywordsServingBaseParams(ServingParams):
    class Config:
        # -> "onclusiveml_serving_keywords" at the time of writing
        env_prefix = f"{ServingParams.__config__.env_prefix}_keywords_"
        env_file_encoding = "utf-8"


class KeywordsServedModelParams(KeywordsServingBaseParams):

    model_artifact_directory: Union[str, Path] = "src/keywords_model_artifacts"
    document_pipeline_artifact: Union[str, Path] = "compiled_document_pipeline"
    word_pipeline_artifact: Union[str, Path] = "compiled_word_pipeline"
    model_card: str = "model_card.json"


class KeywordsServingParams(KeywordsServingBaseParams):

    add_model_predict: bool = True
    add_model_bio: bool = True
