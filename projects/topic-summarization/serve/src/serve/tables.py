"""Topic summarization table."""

# Standard Library
import uuid
from typing import Dict, Optional, Union

# 3rd party libraries
from dyntastic import Dyntastic
from pydantic import Field, validator

# Internal libraries
from onclusiveml.serving.serialization.topic_summarization.v1 import (
    ImpactCategoryLabel,
)

# Source
from src.settings import get_settings


settings = get_settings()


class TopicSummaryDynamoDB(Dyntastic):
    """Prediction request data."""

    __table_name__ = "topic_summary"
    __hash_key__ = "query_id"
    __table_region__ = settings.AWS_DEFAULT_REGION
    __table_host__ = settings.DYNAMODB_HOST

    topic_summary_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    topic_id: int
    trending: Optional[bool]
    topic: Optional[
        Dict[str, Optional[Union[str, Dict[str, str]]]]
    ] = settings.EMPTY_FIELD_TEXT
    impact_category: Optional[ImpactCategoryLabel] = settings.EMPTY_FIELD_TEXT
    query_id: Optional[str] = settings.EMPTY_FIELD_TEXT
    query_string: str

    @validator("topic", "impact_category", "query_id", pre=True)
    def convert_none(cls, v: Optional[str]) -> str:
        """Convert None into N/A string due to Dunytastic not supported empty field."""
        if v is None:
            return settings.EMPTY_FIELD_TEXT
        return v
