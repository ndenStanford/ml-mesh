"""Settings."""

# Standard Library
from functools import lru_cache
from pathlib import Path
from typing import List, Union

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSettings
from onclusiveml.nlp.language.constants import LanguageIso
from onclusiveml.serving.rest.serve.params import ServingParams
from onclusiveml.tracking import (
    TrackedGithubActionsSpecs,
    TrackedImageSpecs,
    TrackedModelSettings,
    TrackingSettings,
)


SUPPORTED_LANGUAGES = [
    LanguageIso.EN,  # English
    LanguageIso.ES,  # Spanish
    LanguageIso.FR,  # French
    LanguageIso.IT,  # Italian
    LanguageIso.DE,  # German
    LanguageIso.CA,  # Catalan
]


class GchSummarizationSettings(TrackingSettings):
    """NER settings."""

    supported_languages: List[LanguageIso] = SUPPORTED_LANGUAGES


class ServerModelSettings(ServingParams):
    """Prediction model settings."""

    model_name: str = "gch-summarization"
    model_directory: Union[str, Path] = "."


class GlobalSettings(
    ServerModelSettings,
    TrackedGithubActionsSpecs,
    TrackedImageSpecs,
    GchSummarizationSettings,
    TrackedModelSettings,
):
    """Global server settings."""


@lru_cache
def get_settings() -> OnclusiveBaseSettings:
    """Returns instanciated global settings class."""
    return GlobalSettings()
