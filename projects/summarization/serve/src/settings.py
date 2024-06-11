"""Settings."""

# Standard Library
from functools import lru_cache
from pathlib import Path
from typing import Dict, Optional, Union

# 3rd party libraries
from pydantic import BaseSettings

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
    api_version: str = "v1"
    api_key_name: str = "x-api-key"
    # Prompt url
    prompt_api: Optional[str]
    internal_ml_endpoint_api_key: str = "1234"
    summarization_default_model: str = "gpt-4-1106-preview"

    summarization_prompts: Dict[str, Dict[str, Dict[str, str]]] = {
        "en": {
            "en": {"alias": "ml-summarization-english"},
            "fr": {"alias": "ml-summarization-english-french"},
        },
        "fr": {
            "fr": {"alias": "ml-summarization-french"},
            "en": {"alias": "ml-summarization-french-english"},
        },
        "de": {"de": {"alias": "ml-summarization-german"}},
        "it": {"it": {"alias": "ml-summarization-italian"}},
        "es": {"es": {"alias": "ml-summarization-spanish"}},
        "ca": {"ca": {"alias": "ml-summarization-catalan"}},
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
def get_settings() -> BaseSettings:
    """Returns instanciated global settings class."""
    settings = GlobalSettings()
    print("Prompt api", settings.prompt_api)
    print("Api key", settings.internal_ml_endpoint_api_key)
    return GlobalSettings()
