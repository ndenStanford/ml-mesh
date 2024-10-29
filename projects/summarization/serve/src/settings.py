"""Settings."""

# Standard Library
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Union

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

    output_schema_with_title: Dict[str, str] = {
        "summary": "Summary of the article(s).",
        "title": "Consolidated title of the article(s).",
    }

    supported_summary_types: List[str] = ["section", "bespoke", "auto", "snippet"]
    snippet_summary_type: str = "snippet"
    snippet_summary_length: int = 50

    summarization_prompts: Dict[LanguageIso, Dict[str, Union[str, Dict[str, str]]]] = {
        LanguageIso.EN: {
            "section": "ml-summarization-english",
            "bespoke": "bespoke-summary-uk",
            "multi-article-summary": {
                "section": "ml-multi-articles-summarization",
                "auto": "ml-multi-articles-summarization",
                "snippet": "ml-multi-articles-summarization",
                "bespoke": "ml-multi-articles-summarization-bespoke",
            },
            "auto": "ml-multi-articles-summarization",
            "snippet": "ml-multi-articles-summarization",
        },
        LanguageIso.FR: {
            "section": "ml-summarization-french",
            "bespoke": "bespoke-summary-fr",
        },
        LanguageIso.DE: {
            "section": "ml-summarization-german",
            "bespoke": "bespoke-summary-de",
        },
        LanguageIso.IT: {
            "section": "ml-summarization-italian",
            "bespoke": "bespoke-summary-it-theme",
        },
        LanguageIso.ES: {
            "section": "ml-summarization-spanish",
            "bespoke": "bespoke-summary-es",
        },
        LanguageIso.CA: {
            "section": "ml-summarization-catalan",
            "bespoke": "bespoke-summary-ca",
        },
        LanguageIso.PT: {"section": "ml-summarization-portuguese"},
        LanguageIso.ZH: {"section": "ml-summarization-chinese_simplified"},
        LanguageIso.JA: {"section": "ml-summarization-japanese"},
        LanguageIso.KO: {"section": "ml-summarization-korean"},
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
