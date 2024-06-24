"""Settings."""

# Standard Library
from functools import lru_cache
from pathlib import Path
from typing import List, Union

# 3rd party libraries
from neptune.types.mode import Mode
from pydantic import Field

# Internal libraries
from onclusiveml.core.base.pydantic import OnclusiveBaseSettings
from onclusiveml.nlp.language.constants import LanguageIso
from onclusiveml.serving.params import ServingBaseParams  # noqa
from onclusiveml.serving.rest.serve.params import ServingParams  # noqa
from onclusiveml.tracking import (
    TrackedGithubActionsSpecs,
    TrackedImageSpecs,
    TrackedModelSettings,
    TrackingSettings,
)


EL_SUPPORTED_LANGUAGES = [
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
    LanguageIso.AR,  # Arabic
]


class TrackedTrainedModelSpecs(TrackedModelSettings):
    """Tracked compiled model settings."""

    # we need an additional version tag since we are referencing an EXISTING model version, rather
    # than creating a new one
    with_id: str = Field("EL-TRAINED-")
    # we only need to download from the base model, not upload
    mode: str = Field(Mode.READ_ONLY)


class ServerModelSettings(ServingParams):
    """Serve model parameters."""

    model_name: str = "entity-linking"
    model_directory: Union[str, Path] = "."
    md_threshold: float = 0.2
    el_threshold: float = 0.4
    checkpoint_name: str = "wiki"
    device: str = "cuda:0"
    config_name: str = "joint_el_mel_new"


class ELSettings(TrackingSettings):
    """Sentiment settings."""

    supported_languages: List[LanguageIso] = EL_SUPPORTED_LANGUAGES


class GlobalSettings(
    ServerModelSettings,
    TrackedTrainedModelSpecs,
    ELSettings,
    TrackedGithubActionsSpecs,
    TrackedImageSpecs,
):
    """Global server settings."""


@lru_cache
def get_settings() -> OnclusiveBaseSettings:
    """Returns instanciated global settings class."""
    return GlobalSettings()
