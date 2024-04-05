"""Service initialization."""
# isort: skip_file

# Internal libraries
from onclusiveml.data.query_profile import MediaAPISettings

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


class ElasticsearchSettings(OnclusiveBaseSettings):
    """Elasticsearch Settings."""

    ELASTICSEARCH_KEY: SecretStr = Field(default="...", exclude=True)
    es_index: List = [
        "crawler",
        "crawler-4-2024.03",
        "crawler-4-2024.02",
        "crawler-4-2024.01",
    ]
    NUM_DOCUMENTS: int = 10
    trend_lookback_days: int = 14
    trend_time_interval: str = "12h"


class GlobalSettings(
    ServerModelSettings,
    TrackedGithubActionsSpecs,
    TrackedImageSpecs,
    MediaAPISettings,
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
