"""Settings."""

# Standard Library
import os
from typing import List

# Internal libraries
from onclusiveml.tracking import (
    TrackedModelCard,
    TrackedModelSpecs,
    TrackedParams,
)


# --- settings classes
class TrackedNERModelSpecs(TrackedModelSpecs):
    """Tracked NER model specs."""

    project: str = "onclusive/ner"
    model = "NER-TRAINED"

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class Inputs(TrackedParams):
    """Inputs."""

    sample_documents_en: List[str] = [""]
    sample_documents_kj: List[str] = [""]

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class NERSettings(TrackedParams):
    """NER settings."""

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class NERModelParams(TrackedParams):
    """Ner model settings."""

    ner_settings: NERSettings = NERSettings()

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class NERModelParams(NERModelParams):
    """Dslim NER model."""

    huggingface_pipeline_task: str = "token-classification"
    huggingface_model_reference: str = "dslim/bert-base-NER"


class NERModelParamsKJ(NERModelParams):
    """Korean/Japanese NER model."""

    huggingface_pipeline_task: str = "token-classification"
    huggingface_model_reference: str = (
        "Davlan/distilbert-base-multilingual-cased-ner-hrl"
    )


class TrackedNERBaseModelCard(TrackedModelCard):
    """The model card for the base model of the NER ML project."""

    model_type: str = "trained"
    # --- custom fields
    # model params
    ner_model_params: NERModelParams = NERModelParams()
    ner_model_params_kj: NERModelParamsKJ = NERModelParamsKJ()
    model_inputs: Inputs = Inputs()
    # admin
    local_output_dir: str = os.path.join(".", "ner_model_artifacts")
    logging_level: str = "INFO"

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"
