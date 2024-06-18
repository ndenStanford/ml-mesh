"""Settings."""

# Standard Library
import os
from functools import lru_cache
from typing import Any, List

# 3rd party libraries
from pydantic import BaseSettings, validator

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

    sample_documents: List[str]
    
    # Custom validator to apply eval to string inputs only
    @validator("sample_documents", pre=True)
    def eval_fields(cls, value: Any) -> Any:
        """Eval input parameters to support Sagemaker estimator constraint."""
        if isinstance(value, str):
            try:
                return eval(value)
            except Exception as e:
                raise ValueError(f"Error evaluating value {value}: {e}")
        return value

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
    model_class: str = "BertForTokenClassification"


class TrackedNERBaseModelCard(TrackedModelCard):
    """The model card for the base model of the NER ML project."""

    model_type: str = "trained"
    # --- custom fields
    # model params
    ner_model_params: NERModelParams = NERModelParams()
    # ner_model_params_kj: NERModelParamsKJ = NERModelParamsKJ()
    model_inputs: Inputs = Inputs()
    # admin
    local_output_dir: str = os.path.join(".", "ner_model_artifacts")
    logging_level: str = "INFO"

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class GlobalSettings(TrackedNERModelSpecs, TrackedNERBaseModelCard):
    """Global server settings."""

    model_specs: TrackedNERModelSpecs = TrackedNERModelSpecs()
    model_card: TrackedNERBaseModelCard = TrackedNERBaseModelCard()


@lru_cache
def get_settings() -> BaseSettings:
    """Returns instanciated global settings class."""
    return GlobalSettings()
