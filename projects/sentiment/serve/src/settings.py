"""Settings."""

# Standard Library
from functools import lru_cache
from pathlib import Path
from typing import Union

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
)


SENT_SUPPORTED_LANGUAGE = [
    LanguageIso.AR,  # Arabic
    LanguageIso.HY,  # Armenian
    LanguageIso.EU,  # Basque
    LanguageIso.BN,  # Bengali
    LanguageIso.MY,  # Burmese
    LanguageIso.CA,  # Catalan
    LanguageIso.ZH,  # Chinese
    LanguageIso.HR,  # Croatian (assuming Croatian for Serbian)
    LanguageIso.CS,  # Czech
    LanguageIso.DA,  # Danish
    LanguageIso.NL,  # Dutch
    LanguageIso.EN,  # English
    LanguageIso.ET,  # Estonian
    LanguageIso.FI,  # Finnish
    LanguageIso.FR,  # French
    # LanguageIso.KA,  # Georgian
    LanguageIso.DE,  # German
    LanguageIso.EL,  # Greek
    LanguageIso.GU,  # Gujarati
    # LanguageIso.HT,  # Haitian
    LanguageIso.HE,  # Hebrew
    LanguageIso.HI,  # Hindi
    LanguageIso.HU,  # Hungarian
    # LanguageIso.IS,  # Icelandic
    LanguageIso.ID,  # Indonesian
    # LanguageIso.GA,  # Irish (assuming Irish for Gaelic)
    LanguageIso.IT,  # Italian
    LanguageIso.JA,  # Japanese
    LanguageIso.KN,  # Kannada
    LanguageIso.KK,  # Kazakh (assuming Kazakh for Kurdish)
    # LanguageIso.KM,  # Khmer
    LanguageIso.KO,  # Korean
    LanguageIso.KU,  # Kurdish
    # LanguageIso.LO,  # Lao
    LanguageIso.LV,  # Latvian
    LanguageIso.LT,  # Lithuanian
    LanguageIso.MK,  # Macedonian (assuming Macedonian for Macedonian)
    LanguageIso.MS,  # Malay (assuming Malay for Malayalam)
    LanguageIso.ML,  # Malayalam
    LanguageIso.MR,  # Marathi
    LanguageIso.NE,  # Nepali
    LanguageIso.NO,  # Norwegian
    # LanguageIso.OR,  # Oriya
    # LanguageIso.PS,  # Pushto
    LanguageIso.PA,  # Panjabi
    LanguageIso.PL,  # Polish
    LanguageIso.PT,  # Portuguese
    LanguageIso.RO,  # Romanian
    LanguageIso.RU,  # Russian
    LanguageIso.SA,  # Sanskrit (assuming Sanskrit for Sindhi)
    # LanguageIso.SR,  # Serbian
    # LanguageIso.SI,  # Sinhala
    LanguageIso.SK,  # Slovak (assuming Slovak for Slovenian)
    LanguageIso.SL,  # Slovenian
    LanguageIso.ES,  # Spanish
    LanguageIso.SV,  # Swedish
    LanguageIso.TA,  # Tamil
    LanguageIso.TE,  # Telugu
    LanguageIso.TH,  # Thai
    LanguageIso.TR,  # Turkish
    LanguageIso.UK,  # Ukrainian
    LanguageIso.UR,  # Urdu
    LanguageIso.UZ,  # Uzbek (assuming Uzbek for Uighur)
    LanguageIso.VI,  # Vietnamese
    LanguageIso.CY,  # Welsh
]


class TrackedCompiledModelSpecs(TrackedModelSpecs):
    """Tracked compiled model settings."""

    # we need an additional version tag since we are referencing an EXISTING model version, rather
    # than creating a new one
    with_id: str = Field("SEN-COMPILED-46", env="neptune_model_version_id")
    # we only need to download from the base model, not upload
    mode: str = Field(Mode.READ_ONLY, env="neptune_client_mode")


class ServerModelSettings(ServingParams):
    """Prediction model settings."""

    model_name: str = "sentiment"
    model_directory: Union[str, Path] = "."


class GlobalSettings(
    ServerModelSettings,
    TrackedCompiledModelSpecs,
    TrackedGithubActionsSpecs,
    TrackedImageSpecs,
):
    """Global server settings."""


@lru_cache
def get_settings() -> BaseSettings:
    """Returns instanciated global settings class."""
    return GlobalSettings()
