"""Settings."""

# Standard Library
from functools import lru_cache
from pathlib import Path
from typing import List, Union

# 3rd party libraries
from neptune.types.mode import Mode

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSettings
from onclusiveml.core.logging import OnclusiveLogSettings
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
    LanguageIso.FR,  # French
    LanguageIso.DE,  # German
    LanguageIso.IT,  # Italian
    LanguageIso.ES,  # Spanish
    LanguageIso.CA,  # Catalan
    LanguageIso.PT,  # Portuguese
    LanguageIso.ZH,  # Chinese (Simplified and Traditional)
    LanguageIso.JA,  # Japanese
    LanguageIso.KO,  # Korean
    LanguageIso.AR,  # Arabic
]


class ServerModelSettings(ServingParams):
    """Prediction model settings."""

    model_name: str = "topic"
    model_directory: Union[str, Path] = "."


class TopicSettings(TrackingSettings):
    """Topic settings."""

    supported_languages: List[LanguageIso] = SUPPORTED_LANGUAGES


class TopicTrackedModelSettings(TrackedModelSettings):
    """Tracked compiled model settings."""

    with_id: str
    mode: str = Mode.READ_ONLY


class GlobalSettings(
    ServerModelSettings,
    TrackedGithubActionsSpecs,
    TrackedImageSpecs,
    TopicSettings,
    OnclusiveLogSettings,
    TopicTrackedModelSettings,
):
    """Global server settings."""


@lru_cache
def get_settings() -> OnclusiveBaseSettings:
    """Returns instanciated global settings class."""
    return GlobalSettings()
