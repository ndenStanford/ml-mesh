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
    TrackedModelSpecs,
    TrackedParams,
)


EL_SUPPORTED_LANGUAGE = [
    LanguageIso.AF,  # Afrikaans
    LanguageIso.AR,  # Arabic
    LanguageIso.BG,  # Bulgarian
    LanguageIso.BN,  # Bengali
    LanguageIso.CA,  # Catalan
    LanguageIso.CS,  # Czech
    LanguageIso.CY,  # Welsh
    LanguageIso.DA,  # Danish
    LanguageIso.DE,  # German
    LanguageIso.EL,  # Greek
    LanguageIso.EN,  # English
    LanguageIso.ES,  # Spanish
    LanguageIso.ET,  # Estonian
    LanguageIso.FA,  # Farsi (Persian)
    LanguageIso.FI,  # Finnish
    LanguageIso.FR,  # French
    LanguageIso.GU,  # Gujarati
    LanguageIso.HE,  # Hebrew
    LanguageIso.HI,  # Hindi
    LanguageIso.HR,  # Croatian
    LanguageIso.HU,  # Hungarian
    LanguageIso.ID,  # Indonesian
    LanguageIso.IT,  # Italian
    LanguageIso.JA,  # Japanese
    LanguageIso.KN,  # Kannada
    LanguageIso.KO,  # Korean
    LanguageIso.LT,  # Lithuanian
    LanguageIso.LV,  # Latvian
    LanguageIso.MK,  # Macedonian
    LanguageIso.ML,  # Malayalam
    LanguageIso.MR,  # Marathi
    LanguageIso.NL,  # Dutch
    LanguageIso.NO,  # Norwegian (Bokmål)
    LanguageIso.PA,  # Punjabi
    LanguageIso.PL,  # Polish
    LanguageIso.PT,  # Portuguese (Brazil)
    LanguageIso.RO,  # Romanian
    LanguageIso.RU,  # Russian
    LanguageIso.SK,  # Slovak
    LanguageIso.SL,  # Slovenian
    LanguageIso.SO,  # Somali
    LanguageIso.SQ,  # Albanian
    LanguageIso.SV,  # Swedish
    LanguageIso.SW,  # Swahili
    LanguageIso.TA,  # Tamil
    LanguageIso.TE,  # Telugu
    LanguageIso.TH,  # Thai
    LanguageIso.TR,  # Turkish
    LanguageIso.UK,  # Ukrainian
    LanguageIso.UR,  # Urdu
    LanguageIso.VI,  # Vietnamese
    LanguageIso.ZH,  # Chinese (Simplified)
    LanguageIso.TL,  # Tagalog
    LanguageIso.HT,  # Haitian Creole
    LanguageIso.SR,  # Serbian
    LanguageIso.IS,  # Icelandic
    LanguageIso.SI,  # Sinhala
    LanguageIso.AM,  # Amharic
    LanguageIso.HY,  # Armenian
    LanguageIso.KA,  # Georgian
    LanguageIso.PS,  # Pashto
]


class TrackedTrainedModelSpecs(TrackedModelSpecs):
    """Tracked compiled model settings."""

    # we need an additional version tag since we are referencing an EXISTING model version, rather
    # than creating a new one
    with_id: str = Field("EL-TRAINED-", env="neptune_model_version_id")
    # we only need to download from the base model, not upload
    mode: str = Field(Mode.READ_ONLY, env="neptune_client_mode")


class ServerModelSettings(ServingParams):
    """Serve model parameters."""

    model_name: str = "entity-linking"
    model_directory: Union[str, Path] = "."
    md_threshold: float = 0.2
    el_threshold: float = 0.4
    checkpoint_name: str = "wiki"
    device: str = "cuda:0"
    config_name: str = "joint_el_mel_new"


class ELSettings(TrackedParams):
    """Sentiment settings."""

    supported_languages: List[LanguageIso] = EL_SUPPORTED_LANGUAGE


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
