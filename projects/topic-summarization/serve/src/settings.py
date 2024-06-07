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
from typing import Dict, List, Optional


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
    CLAUDE_TOPIC_ALIAS: str = "ml-topic-summarization-claude"
    GPT_TOPIC_ALIAS: str = "ml-topic-summarization-gpt"
    CLAUDE_SUMMARY_ALIAS: str = "ml-topic-summarization-multi-articles-summary-claude"
    GPT_SUMMARY_ALIAS: str = "ml-topic-summarization-multi-articles-summary-gpt"
    DEFAULT_MODEL: str = "anthropic.claude-3-sonnet-20240229-v1:0"
    GPT_MODEL: str = "gpt-4-turbo-2024-04-09"

    model_settings = ServerModelSettings()

    TOPIC_RESPONSE_SCHEMA: Dict[str, str] = {}
    for category_key, category_value in model_settings.IMPACT_CATEGORIES.items():
        category_dict = {
            f"{category_key}_summary": f"The summary for the content about {category_value}, based on the input articles",  # noqa: E501
            f"{category_key}_theme": f"An overall theme for {category_value}",
            f"{category_key}_impact": f"The impact level of {category_value}",
        }
        TOPIC_RESPONSE_SCHEMA.update(category_dict)

    SUMMARY_RESPONSE_SCHEMA: Dict[str, str] = {
        "summary": "Your synthesized summary based on all the summaries I provided",
        "theme": "The theme for your consolidated summary",
    }


class ElasticsearchSettings(OnclusiveBaseSettings):
    """Elasticsearch Settings."""

    ELASTICSEARCH_KEY: SecretStr = Field(
        default="...", env="ELASTICSEARCH_KEY", exclude=True
    )
    es_index: List = [
        "crawler-4-2024.05",
        "crawler-4-2024.04",
        "crawler-4-2024.03",
        "crawler-4-2024.02",
        "crawler-4-2024.01",
        "crawler",
    ]


class DynamoDBSettings(OnclusiveBaseSettings):
    """DynamoDB Settings."""

    AWS_DEFAULT_REGION: str = "us-east-1"
    DYNAMODB_HOST: Optional[str] = None


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
    # number of days to look past the inflection point when collecting documents (at 00:00)
    DAYS_PAST_INFLECTION_POINT: int = 2

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
    DynamoDBSettings,
    ImpactQuantificationSettings,
    TrendSummarizationSettings,
):
    """Global server settings."""


@lru_cache
def get_settings() -> OnclusiveFrozenSettings:
    """Returns instanciated global settings class."""
    return GlobalSettings()


@lru_cache
def get_api_settings() -> OnclusiveFrozenSettings:
    """Returns API settings."""
    return PromptBackendAPISettings()
