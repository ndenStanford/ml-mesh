# Standard Library
from pathlib import Path
from typing import Union

# Internal libraries
from onclusiveml.serving.rest.serve import ServingBaseParams


class ServedModelParams(ServingBaseParams):

    model_name: str = "keywords_model"
    model_artifact_directory: Union[str, Path] = "src/keywords_model_artifacts"
    document_pipeline_artifact: Union[str, Path] = "compiled_document_pipeline"
    word_pipeline_artifact: Union[str, Path] = "compiled_word_pipeline"
    model_card: str = "model_card.json"
