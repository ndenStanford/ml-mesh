"""Settings."""

# Standard Library
import os
from functools import lru_cache

# 3rd party libraries
from pydantic_settings import BaseSettings, SettingsConfigDict

# Internal libraries
from onclusiveml.tracking import (
    TrackedModelCard,
    TrackedModelSettings,
    TrackingSettings,
)


# --- settings classes
class TrackedNERModelSpecs(TrackedModelSettings):
    """Tracked NER model specs."""

    project: str = "onclusive/ner"
    model: str = "NER-TRAINED"
    model_config = SettingsConfigDict(protected_namespaces=("settings_",))


class Inputs(TrackingSettings):
    """Inputs."""

    sample_document: str


class NERSettings(TrackingSettings):
    """NER settings."""


class NERModelParams(TrackingSettings):
    """Ner model settings."""

    ner_settings: NERSettings = NERSettings()


class NERModelParams(NERModelParams):
    """Dslim NER model."""

    huggingface_pipeline_task: str = "token-classification"
    huggingface_model_reference: str = "dslim/bert-base-NER"
    model_class: str = "BertForTokenClassification"
    model_config = SettingsConfigDict(protected_namespaces=("settings_",))


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

    model_config = SettingsConfigDict(
        protected_namespaces=("settings_",),
        env_file="config/dev.env",
        env_file_encoding="utf-8",
    )


class GlobalSettings(TrackedNERModelSpecs, TrackedNERBaseModelCard):
    """Global server settings."""

    model_specs: TrackedNERModelSpecs = TrackedNERModelSpecs()
    model_card: TrackedNERBaseModelCard = TrackedNERBaseModelCard()

    model_config = SettingsConfigDict(protected_namespaces=("settings_",))


@lru_cache
def get_settings() -> BaseSettings:
    """Returns instanciated global settings class."""
    return GlobalSettings()
