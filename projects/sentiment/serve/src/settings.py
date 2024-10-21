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
    LanguageIso.PT,  # Portuguese
    LanguageIso.ES,  # Spanish
    LanguageIso.AR,  # Arabic
    LanguageIso.KO,  # Korean
    LanguageIso.TH,  # Thai
    LanguageIso.JA,  # Japanese
    LanguageIso.TL,  # Tagalog
    LanguageIso.TR,  # Turkish
    LanguageIso.FR,  # French
    LanguageIso.RU,  # Russian
    LanguageIso.IT,  # Italian
    LanguageIso.ID,  # Indonesian
    LanguageIso.PL,  # Polish
    LanguageIso.HI,  # Hindi
    LanguageIso.NL,  # Dutch
    LanguageIso.HT,  # Haitian
    LanguageIso.UR,  # Urdu
    LanguageIso.DE,  # German
    LanguageIso.FA,  # Persian
    LanguageIso.CA,  # Catalan
    LanguageIso.SV,  # Swedish
    LanguageIso.FI,  # Finnish
    LanguageIso.ET,  # Estonian
    LanguageIso.EL,  # Greek
    LanguageIso.CS,  # Czech
    LanguageIso.EU,  # Basque
    LanguageIso.TA,  # Tamil
    LanguageIso.HE,  # Hebrew
    LanguageIso.ZH,  # Chinese
    LanguageIso.NO,  # Norwegian
    LanguageIso.DA,  # Danish
    LanguageIso.CY,  # Welsh
    LanguageIso.LV,  # Latvian
    LanguageIso.HU,  # Hungarian
    LanguageIso.RO,  # Romanian
    LanguageIso.LT,  # Lithuanian
    LanguageIso.VI,  # Vietnamese
    LanguageIso.UK,  # Ukrainian
    LanguageIso.NE,  # Nepali
    LanguageIso.SR,  # Serbian
    LanguageIso.BN,  # Bengali
    LanguageIso.SL,  # Slovenian
    LanguageIso.IS,  # Icelandic
    LanguageIso.ML,  # Malayalam
    LanguageIso.BG,  # Bulgarian
    LanguageIso.MR,  # Marathi
    LanguageIso.SI,  # Sinhala
    LanguageIso.OR,  # Oriya
    LanguageIso.LO,  # Lao
    LanguageIso.TE,  # Telugu
    LanguageIso.KN,  # Kannada
    LanguageIso.KU,  # Kurdish
    LanguageIso.PS,  # Pashto
    LanguageIso.GU,  # Gujarati
    LanguageIso.AM,  # Amharic
    LanguageIso.SD,  # Sindhi
    LanguageIso.PA,  # Punjabi
    LanguageIso.MY,  # Burmese
    LanguageIso.KM,  # Khmer
    LanguageIso.HY,  # Armenian
    LanguageIso.KA,  # Georgian
    LanguageIso.DV,  # Dhivehi
    LanguageIso.UG,  # Uighur
]


class SentimentSettings(TrackingSettings):
    """Sentimentiment settings."""

    supported_languages: List[LanguageIso] = SUPPORTED_LANGUAGES
    MIN_CHARACTERS: int = 10


class TrackedCompiledModelSpecs(TrackedModelSettings):
    """Tracked compiled model settings."""

    # we need an additional version tag since we are referencing an EXISTING model version, rather
    # than creating a new one
    with_id: str
    # we only need to download from the base model, not upload
    mode: str = Mode.READ_ONLY


class ServerModelSettings(ServingParams):
    """Prediction model settings."""

    model_name: str = "sentiment"
    model_directory: Union[str, Path] = "."


class GlobalSettings(
    ServerModelSettings,
    TrackedGithubActionsSpecs,
    TrackedImageSpecs,
    SentimentSettings,
    OnclusiveLogSettings,
    TrackedCompiledModelSpecs,
):
    """Global server settings."""


@lru_cache
def get_settings() -> OnclusiveBaseSettings:
    """Returns instanciated global settings class."""
    return GlobalSettings()
