"""Settings."""

# Standard Library
from functools import lru_cache
from pathlib import Path
from typing import Dict, Optional, Union

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSettings
from onclusiveml.nlp.language import LanguageIso
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
    translation_api: str = "translation-serve:8001"
    internal_ml_endpoint_api_key: str = "1234"
    summarization_default_model: str = "gpt-4o-mini"
    multi_article_summary: str = "multi-article-summary"

    summarization_prompts: Dict[LanguageIso, Dict[str, str]] = {
        LanguageIso.EN: {
            "section": "ml-summarization-english",
            "bespoke": "bespokse-summary-uk",
            "multi-article-summary": "ml-multi-articles-summarization",
        },
        LanguageIso.FR: {
            "section": "ml-summarization-french",
            "bespoke": "bespokse-summary-fr",
        },
        LanguageIso.DE: {
            "section": "ml-summarization-german",
            "bespoke": "bespokse-summary-de",
        },
        LanguageIso.IT: {
            "section": "ml-summarization-italian",
            "bespoke": "bespokse-summary-it-theme",
        },
        LanguageIso.ES: {
            "section": "ml-summarization-spanish",
            "bespoke": "bespokse-summary-es",
        },
        LanguageIso.CA: {
            "section": "ml-summarization-catalan",
            "bespoke": "bespokse-summary-ca",
        },
        LanguageIso.PT: {"section": "ml-summarization-portuguese"},
        LanguageIso.ZH: {"section": "ml-summarization-chinese_simplified"},
        LanguageIso.JA: {"section": "ml-summarization-japanese"},
        LanguageIso.KO: {"section": "ml-summarization-korean"},
    }


class AWSSettings(OnclusiveBaseSettings):
    """AWS settings to retrieve data for test."""

    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    REGION_NAME: Optional[str] = None

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class RedshiftSettings(OnclusiveBaseSettings):
    """Redshift settings to retrieve data for test."""

    CLUSTER_ID: Optional[str] = None
    DATABASE: Optional[str] = None
    DB_USER: Optional[str] = None
    SQL: Optional[str] = None

    class Config:
        env_prefix = "redshift_"
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class DeepEvalSettings(OnclusiveBaseSettings):
    """Deepeval settings for integration test."""

    PERCENT_SUCCESS: Optional[str] = None
    THRESHOLD: Optional[str] = None
    MODEL: Optional[str] = None
    SUMMARIZATION_COMPRESSION_RATIO: Optional[str] = 4

    class Config:
        env_prefix = "deepeval_"
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class GlobalSettings(
    ServerModelSettings,
    ApplicationSettings,
    AWSSettings,
    RedshiftSettings,
    DeepEvalSettings,
):
    """Global server settings."""


@lru_cache
def get_settings() -> OnclusiveBaseSettings:
    """Returns instanciated global settings class."""
    return GlobalSettings()
