"""Settings."""

# Standard Library
from functools import lru_cache
from pathlib import Path
from typing import List, Union

# 3rd party libraries
from pydantic import BaseSettings

# Internal libraries
from onclusiveml.nlp.language.constants import LanguageIso
from onclusiveml.serving.rest.serve.params import ServingParams
from onclusiveml.tracking import (
    TrackedGithubActionsSpecs,
    TrackedImageSpecs,
    TrackedParams,
)


LSH_SUPPORTED_LANGUAGES = [
    LanguageIso.EN,  # English
    LanguageIso.FR,  # French
    LanguageIso.DE,  # German
    LanguageIso.IT,  # Italian
    LanguageIso.ES,  # Spanish
    LanguageIso.CA,  # Catalan
    LanguageIso.PT,  # Portuguese
    LanguageIso.ZH,  # Chinese
    LanguageIso.JA,  # Japanese
    LanguageIso.KO,  # Korean
]


class ServerModelSettings(ServingParams):
    """Serve model parameters."""

    model_name: str = "lsh"
    model_directory: Union[str, Path] = "."


class LSHSettings(TrackedParams):
    """Sentiment settings."""

    supported_languages: List[LanguageIso] = LSH_SUPPORTED_LANGUAGES


class GlobalSettings(
    ServerModelSettings,
    LSHSettings,
    TrackedGithubActionsSpecs,
    TrackedImageSpecs,
):
    """Global server settings."""


@lru_cache
def get_settings() -> BaseSettings:
    """Returns instanciated global settings class."""
    return GlobalSettings()
