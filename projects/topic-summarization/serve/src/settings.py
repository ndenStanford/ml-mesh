"""Service initialization."""
# isort: skip_file

# Standard Library
from functools import lru_cache

# Internal libraries
from onclusiveml.core.base import OnclusiveFrozenSettings, OnclusiveBaseSettings
from onclusiveml.serving.rest.serve.params import ServingParams
from onclusiveml.tracking import TrackedGithubActionsSpecs, TrackedImageSpecs
from pydantic import SecretStr, Field
from typing import List

# Source
from src.serve.category_storage import Category_list


class ServerModelSettings(ServingParams):
    """Serve model parameters."""

    model_name: str = "topic-summarization"
    CATEGORY_LIST: list = Category_list


class PromptBackendAPISettings(OnclusiveFrozenSettings):
    """API configuration."""

    PROMPT_API: str = "http://prompt-backend:4000"
    INTERNAL_ML_ENDPOINT_API_KEY: str = "1234"
    PROMPT_ALIAS: dict = {
        "single_topic": "ml-topic-summarization-single-analysis",
        "topic_aggregate": "ml-topic-summarization-aggregation",
        "single_summary": "ml-multi-articles-summarization",
        "summary_aggregate": "ml-articles-summary-aggregation",
    }


class MediaApiSettings(OnclusiveBaseSettings):
    """Media API."""

    MEDIA_API_URI: str = "https://staging-querytool-api.platform.onclusive.org"
    ML_QUERY_ID: str = "6bcd99ee-df08-4a7e-ad5e-5cdab4b558c3"
    MEDIA_CLIENT_ID: SecretStr = Field(
        default="...", exclude=True, env="MEDIA_CLIENT_ID"
    )
    MEDIA_CLIENT_SECRET: SecretStr = Field(
        default="...", exclude=True, env="MEDIA_CLIENT_SECRET"
    )


class ElasticsearchSettings(OnclusiveBaseSettings):
    """Elasticsearch Settings."""

    ELASTICSEARCH_KEY: SecretStr = Field(
        default="...", exclude=True, env="ELASTICSEARCH_KEY"
    )
    es_index: List = [
        "crawler",
        "crawler-4-2024.03",
        "crawler-4-2024.02",
        "crawler-4-2024.01",
    ]
    NUM_DOCUMENTS: int = 5
    trend_lookback_days: int = 14
    trend_time_interval: str = "12h"


class GlobalSettings(
    ServerModelSettings,
    TrackedGithubActionsSpecs,
    TrackedImageSpecs,
    MediaApiSettings,
    ElasticsearchSettings,
):
    """Global server settings."""

    ARTICLE_GROUP_SIZE: int = 8  # how many articles are handled together
    MULTIPROCESS_WORKER: int = 5


@lru_cache
def get_settings() -> OnclusiveFrozenSettings:
    """Returns instanciated global settings class."""
    return GlobalSettings()


@lru_cache
def get_api_settings() -> OnclusiveFrozenSettings:
    """Returns API settings."""
    return PromptBackendAPISettings()
