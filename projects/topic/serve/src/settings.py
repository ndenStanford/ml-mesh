"""Settings."""

# Standard Library
from functools import lru_cache
from pathlib import Path
from typing import List, Union

# 3rd party libraries
from neptune.types.mode import Mode
from pydantic import Field

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


class TrackedTrainedModelSpecs(TrackedModelSettings):
    """Tracked compiled model settings."""

    # we need an additional version tag since we are referencing an EXISTING model version, rather
    # than creating a new one
    with_id: str = Field("TOPIC-TRAINED-63", env="neptune_model_version_id")
    # we only need to download from the base model, not upload
    mode: str = Field(Mode.READ_ONLY, env="neptune_client_mode")


class ServerModelSettings(ServingParams):
    """Prediction model settings."""

    model_name: str = "topic"
    model_directory: Union[str, Path] = "."


class TopicSettings(TrackingSettings):
    """Topic settings."""

    supported_languages: List[LanguageIso] = SUPPORTED_LANGUAGES


class GlobalSettings(
    ServerModelSettings,
    TrackedTrainedModelSpecs,
    TrackedGithubActionsSpecs,
    TrackedImageSpecs,
    TopicSettings,
):
    """Global server settings."""


@lru_cache
def get_settings() -> OnclusiveBaseSettings:
    """Returns instanciated global settings class."""
    return GlobalSettings()
