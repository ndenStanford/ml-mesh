"""Settings."""

# Standard Library
from functools import lru_cache
from pathlib import Path
from typing import Dict, Union

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSettings
from onclusiveml.serving.rest.serve.params import ServingParams


class ServerModelSettings(ServingParams):
    """Serve model parameters."""

    model_name: str = "summarization"
    model_directory: Union[str, Path] = "."


class ApplicationSettings(OnclusiveBaseSettings):
    """App base settings."""

    enable_metrics: bool = False
    api_version: str = "v2"
    api_key_name: str = "x-api-key"
    # Prompt url
    prompt_api: str = "http://prompt-backend:4000"
    translation_api: str = (
        "http://http://translation-service:8000/translation/v1/predict"
    )
    internal_ml_endpoint_api_key: str = "1234"
    summarization_default_model: str = "gpt-4o"

    summarization_prompts: Dict[
        str, Dict[str, Dict[str, Union[str, Dict[str, str]]]]
    ] = {
        "en": {
            "en": {
                "alias": "ml-summarization-english",
                "bespoke-summary": {"alias": "bespokse-summary-uk"},
            },
            "fr": {"alias": "ml-summarization-english-french"},
        },
        "fr": {
            "fr": {
                "alias": "ml-summarization-french",
                "bespoke-summary": {"alias": "bespokse-summary-fr"},
            },
            "en": {"alias": "ml-summarization-french-english"},
        },
        "de": {
            "de": {
                "alias": "ml-summarization-german",
                "bespoke-summary": {"alias": "bespokse-summary-de"},
            }
        },
        "it": {
            "it": {
                "alias": "ml-summarization-italian",
                "bespoke-summary": {"alias": "bespokse-summary-it-theme"},
            }
        },
        "gl": {
            "gl": {
                "bespoke-summary": {"alias": "bespokse-summary-gl"},
            }
        },
        "es": {
            "es": {
                "alias": "ml-summarization-spanish",
                "bespoke-summary": {"alias": "bespokse-summary-es"},
            }
        },
        "ca": {
            "ca": {
                "alias": "ml-summarization-catalan",
                "bespoke-summary": {"alias": "bespokse-summary-ca"},
            }
        },
        "pt": {"pt": {"alias": "ml-summarization-portuguese"}},
        "zh": {"zh": {"alias": "ml-summarization-chinese_simplified"}},
        "zh-t": {"zh-t": {"alias": "ml-summarization-chinese_traditional"}},
        "ja": {"ja": {"alias": "ml-summarization-japanese"}},
        "ko": {"ko": {"alias": "ml-summarization-korean"}},
    }


class GlobalSettings(
    ServerModelSettings,
    ApplicationSettings,
):
    """Global server settings."""


@lru_cache
def get_settings() -> OnclusiveBaseSettings:
    """Returns instanciated global settings class."""
    return GlobalSettings()
