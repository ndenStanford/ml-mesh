"""Settings."""

# Standard Library
from functools import lru_cache
from pathlib import Path
from typing import List, Set, Union

# 3rd party libraries
from pydantic import BaseSettings

# Internal libraries
from onclusiveml.nlp.language.constants import LanguageIso
from onclusiveml.serving.rest.serve.params import ServingParams
from onclusiveml.tracking import TrackedGithubActionsSpecs, TrackedImageSpecs


IPTC_SUPPORTED_LANGUAGE = [
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


class ServerModelSettings(ServingParams):
    """Serve model parameters."""

    model_name: str = "iptc-multi"
    model_directory: Union[str, Path] = "."
    max_topic_num: int = 5
    min_score_cutoff: float = 0.01
    model_endpoint_template: str = "serve-iptc-{}:8000"
    model_endpoint_secure: bool = False
    test_model_sequence: List[str] = []
    sample_inference_content: str = "Test Content"
    historically_high_inferenced_models: Set[str] = {
        "00000000",
        "01000000",
        "04000000",
        "10000000",
        "20000209",
    }
    supported_languages: List[LanguageIso] = IPTC_SUPPORTED_LANGUAGE

    class Config:
        env_prefix = "server_model_settings_"
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class GlobalSettings(
    ServerModelSettings,
    TrackedGithubActionsSpecs,
    TrackedImageSpecs,
):
    """Global server settings."""


@lru_cache
def get_settings() -> BaseSettings:
    """Returns instanciated global settings class."""
    return GlobalSettings()
