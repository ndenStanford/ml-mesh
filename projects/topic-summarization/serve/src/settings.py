"""Service initialization."""
# isort: skip_file

# Internal libraries
from onclusiveml.queries.query_profile import MediaAPISettings

# Standard Library
import itertools
from functools import lru_cache

# Internal libraries
from onclusiveml.core.base import (
    OnclusiveFrozenSettings,
    OnclusiveBaseSettings,
)
from onclusiveml.serving.rest.serve.params import ServingParams
from onclusiveml.tracking import TrackedGithubActionsSpecs, TrackedImageSpecs
from pydantic import SecretStr, Field, root_validator
from typing import Dict, List, Optional
from src.es_utils import generate_crawler_indices


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
    GPT_TOPIC_ALIAS: str = "ml-topic-summarization-citations-gpt"
    GPT_TOPIC_WITH_ENTITY_ALIAS: str = "ml-topic-summarization-entity-focus-gpt"

    CLAUDE_SUMMARY_QUALITY_ALIAS: str = "ml-topic-summarization-summary-quality"
    GPT_SUMMARY_ALIAS: str = "ml-topic-summarization-multi-articles-summary-gpt"
    GPT_SUMMARY_WITH_ENTITY_ALIAS: str = (
        "ml-topic-summarization-multi-articles-summary-entity-focus-gpt"
    )
    SUMMARY_QUALITY_RESPONSE_SCHEMA: Dict[str, str] = {
        "different_themes": "Does the summary contains different themes. Put either 'yes' or 'no'.",
        "entities_related": "Are all parts of the summary related to the entities Put either 'yes' or 'no'.",  # noqa: E501
    }
    CLAUDE_QUERY_ENTITY_EXTRACTION_ALIAS: str = "ml-entity-query-extract-claude"
    GPT_QUERY_ENTITY_EXTRACTION_ALIAS: str = "ml-entity-query-extract-gpt"
    DEFAULT_MODEL: str = "gpt-4o-mini"
    HAIKU_CLAUDE_MODEL: str = "anthropic.claude-3-haiku-20240307-v1:0"
    GPT_MODEL: str = "gpt-4o"

    model_settings: ServerModelSettings = ServerModelSettings()
    # fmt: off
    TOPIC_RESPONSE_SCHEMA: Dict[str, str] = dict(
        itertools.chain.from_iterable(
            [
                [
                    (
                        f"{category_key}_summary",
                        f"The summary for the content about {category_value}, based on the input articles",  # noqa: E501
                    ),
                    (
                        f"{category_key}_theme",
                        f"An overall theme for {category_value}",
                    ),
                    (
                        f"{category_key}_impact",
                        f"The impact level of {category_value}",
                    ),
                    (
                        f"{category_key}_sources",
                        f"The indices of articles used in this summary of {category_value}"
                    ),
                ]
                for category_key, category_value in model_settings.IMPACT_CATEGORIES.items()
            ]
        )
    )
    # fmt: on
    SUMMARY_RESPONSE_SCHEMA: Dict[str, str] = {
        "summary": "Your synthesized summary based on all the summaries I provided",
        "theme": "The theme for your consolidated summary",
    }

    ENTITY_RESPONSE_SCHEMA: Dict[str, str] = {
        "entity_list": "a string representing a list of detected entities"
    }


class ElasticsearchSettings(OnclusiveBaseSettings):
    """Elasticsearch Settings."""

    ELASTICSEARCH_KEY: SecretStr = Field(
        default="...", env="ELASTICSEARCH_KEY", exclude=True
    )
    es_index: List = []
    ES_TIMEOUT: int = 90

    @root_validator(pre=True)
    def set_es_index(cls, values):
        """Dynamic get es index."""
        elasticsearch_key = values.get("ELASTICSEARCH_KEY")
        values["es_index"] = generate_crawler_indices(elasticsearch_key)
        return values


class DynamoDBSettings(OnclusiveBaseSettings):
    """DynamoDB Settings."""

    AWS_DEFAULT_REGION: str = "us-east-1"
    DYNAMODB_HOST: Optional[str] = None
    # table name should be referencing relevant table when deployed
    DYNAMODB_TABLE_NAME: str
    ENVIRONMENT: str = "dev"


class TrendSummarizationSettings(OnclusiveBaseSettings):
    """Trend Summarization Settings."""

    # No of documents to collect for summarization
    NUM_DOCUMENTS: int = 5
    # Lookback days to assess trend
    TREND_LOOKBACK_DAYS: int = 14
    # Number of documents per interval
    TREND_TIME_INTERVAL: str = "12h"
    # Document scale threshold to run trend detection
    TOPIC_DOCUMENT_THRESHOLD: float = 0.01
    # number of days to look past the inflection point when collecting documents (at 00:00)
    DAYS_PAST_INFLECTION_POINT: int = 2


class ImpactQuantificationSettings(OnclusiveBaseSettings):
    """Impact Quantification Settings."""

    impact_lookback_days: int = 125
    time_interval: str = "24h"
    local_raio_cutoff: float = 0.01
    global_local_comparison_ratio_cutoff: float = 1
    mf_tau_cutoff: float = 0.8


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
