# isort: skip_file
"""Topic summarization table."""

# Standard Library
import uuid
from datetime import datetime
from typing import Dict, Optional, Union, List, Any

# 3rd party libraries
from dyntastic import Dyntastic
from pydantic import Field, validator
from decimal import Decimal

# Internal libraries
from onclusiveml.serving.serialization.topic_summarization.v1 import (
    ImpactCategoryLabel,
)

# Source
from src.settings import get_settings

settings = get_settings()


class TopicSummaryDynamoDB(Dyntastic):
    """Prediction request data."""

    __table_name__ = settings.DYNAMODB_TABLE_NAME
    __hash_key__ = "id"
    __table_region__ = "us-east-2"
    __table_host__ = settings.DYNAMODB_HOST

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime
    topic_id: int
    trending: Optional[bool] = None
    analysis: Optional[
        Dict[str, Union[Dict[str, Union[str, ImpactCategoryLabel]], str, None]]
    ] = None
    impact_category: Optional[ImpactCategoryLabel] = None
    query_id: Optional[str] = None
    query_string: str
    trend_lookback_days: int
    topic_document_threshold: Decimal
    trend_time_interval: str
    days_past_inflection_point: int
    content: Optional[List[str]] = None
    query_all_doc_count: Optional[List[Dict[str, Union[str, int]]]] = None
    query_topic_doc_count: Optional[List[Dict[str, Union[str, int]]]] = None

    @validator("query_all_doc_count", "query_topic_doc_count", "trending", pre=False)
    @classmethod
    def serialize_fields(cls, fields: Any) -> str:
        """Serialize certain fields as string objects."""
        return str(fields)

    @validator("query_all_doc_count", "query_topic_doc_count", "trending", pre=True)
    @classmethod
    def deserialize_fields(cls, fields: Union[str, Any]) -> Any:
        """Deserialize certain fields to their evaluated object."""
        if isinstance(fields, str):
            return eval(fields)
        else:
            return fields
