"""Service initialization."""
# isort: skip_file

# Internal libraries
from onclusiveml.data.query_profile import MediaAPISettings

# Standard Library
from functools import lru_cache

# Internal libraries
from onclusiveml.core.base import (
    OnclusiveFrozenSettings,
    OnclusiveBaseSettings,
)
from onclusiveml.serving.rest.serve.params import ServingParams
from onclusiveml.tracking import TrackedGithubActionsSpecs, TrackedImageSpecs
from pydantic import SecretStr, Field
from typing import Dict, List


class ServerModelSettings(ServingParams):
    """Serve model parameters."""

    model_name: str = "topic-summarization"
    IMPACT_CATEGORIES: Dict[str, str] = {
        "opportunities": "Opportunities",
        "risk": "Risk detection",
        "threats": "Threats for the brand",
        "company": "Company or spokespersons",
        "brand": "Brand Reputation",
        "ceo": "CEO Reputation",
        "customer": "Customer Response",
        "stock": "Stock Price Impact",
        "industry": "Industry trends",
        "environment": "Environmental, social and governance",
    }


class PromptBackendAPISettings(OnclusiveFrozenSettings):
    """API configuration."""

    PROMPT_API: str = "http://prompt-backend:4000"
    INTERNAL_ML_ENDPOINT_API_KEY: str = "1234"
    PROMPT_ALIAS: dict = {
        "claude_topic": "ml-topic-summarization-claude",
        "gpt_topic": "ml-topic-summarization-gpt",
    }
    DEFAULT_MODEL: str = "anthropic.claude-3-sonnet-20240229-v1:0"
    GPT_MODEL: str = "gpt-4-turbo-2024-04-09"

    TOPIC_RESPONSE_SCHEMA: Dict[str, str] = {
        category: f"The summary for the content related to {category} in the articles. And the impact level of {category} based on the summary."  # noqa: E501
        for category in ServerModelSettings.IMPACT_CATEGORIES.values()
    }


class ElasticsearchSettings(OnclusiveBaseSettings):
    """Elasticsearch Settings."""

    ELASTICSEARCH_KEY: SecretStr = Field(
        default="...", env="ELASTICSEARCH_KEY", exclude=True
    )
    es_index: List = [
        "crawler",
        "crawler-4-2024.03",
        "crawler-4-2024.02",
        "crawler-4-2024.01",
    ]


class TrendSummarizationSettings(OnclusiveBaseSettings):
    """Trend Summarization Settings."""

    # No of documents to collect for summarization
    NUM_DOCUMENTS: int = 5
    # Lookback days to assess trend
    trend_lookback_days: int = 14
    # Number of documents per interval
    trend_time_interval: str = "12h"
    # Document scale threshold to run trend detection
    TOPIC_DOCUMENT_THRESHOLD: float = 0.01

    class Config:
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class ImpactQuantificationSettings(OnclusiveBaseSettings):
    """Impact Quantification Settings."""

    impact_lookback_days: int = 125
    time_interval: str = "24h"
    local_raio_cutoff = 0.01
    global_local_comparison_ratio_cutoff = 1
    mf_tau_cutoff = 0.8


class GlobalSettings(
    ServerModelSettings,
    TrackedGithubActionsSpecs,
    TrackedImageSpecs,
    MediaAPISettings,
    ElasticsearchSettings,
    ImpactQuantificationSettings,
    TrendSummarizationSettings,
):
    """Global server settings."""

    # ARTICLE_GROUP_SIZE: int = 8  # how many articles are handled together
    # MULTIPROCESS_WORKER: int = 5


@lru_cache
def get_settings() -> OnclusiveFrozenSettings:
    """Returns instanciated global settings class."""
    return GlobalSettings()


@lru_cache
def get_api_settings() -> OnclusiveFrozenSettings:
    """Returns API settings."""
    return PromptBackendAPISettings()
