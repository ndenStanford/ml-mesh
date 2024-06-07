"""Settings."""

# Standard Library
from functools import lru_cache
from pathlib import Path
from typing import List, Union

# 3rd party libraries
from neptune.types.mode import Mode
from pydantic import BaseSettings, Field

# Internal libraries
from onclusiveml.nlp.language.constants import LanguageIso
from onclusiveml.serving.rest.serve.params import ServingParams
from onclusiveml.tracking import (
    TrackedGithubActionsSpecs,
    TrackedImageSpecs,
    TrackedModelSpecs,
    TrackedParams,
)


SUPPORTED_LANGUAGES = [
    LanguageIso.EN,  # English
    LanguageIso.ES,  # Spanish
    LanguageIso.FR,  # French
    LanguageIso.IT,  # Italian
    LanguageIso.DE,  # German
    LanguageIso.CA,  # Catalan
]


class GchSummarizationSettings(TrackedParams):
    """NER settings."""

    supported_languages: List[LanguageIso] = SUPPORTED_LANGUAGES


class TrackedTrainedModelSpecs(TrackedModelSpecs):
    """Tracked compiled model settings."""

    # we need an additional version tag since we are referencing an EXISTING model version, rather
    # than creating a new one
    with_id: str = Field("SUM-TRAINED-79", env="neptune_model_version_id")
    # we only need to download from the base model, not upload
    mode: str = Field(Mode.READ_ONLY, env="neptune_client_mode")


class ServerModelSettings(ServingParams):
    """Prediction model settings."""

    model_name: str = "gch-summarization"
    model_directory: Union[str, Path] = "."


class GlobalSettings(
    ServerModelSettings,
    TrackedTrainedModelSpecs,
    TrackedGithubActionsSpecs,
    TrackedImageSpecs,
    GchSummarizationSettings,
):
    """Global server settings."""


@lru_cache
def get_settings() -> BaseSettings:
    """Returns instanciated global settings class."""
    return GlobalSettings()
