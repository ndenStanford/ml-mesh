# isort: skip_file
"""Topic summarization table."""

# Standard Library
import uuid
from datetime import datetime
from typing import Dict, Optional, Union, Any

# 3rd party libraries
from dyntastic import Dyntastic
from pydantic import Field

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
    __hash_key__ = "topic_summary_id"
    __table_region__ = "us-east-2"
    __table_host__ = settings.DYNAMODB_HOST

    topic_summary_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = datetime.now()
    topic_id: int
    trending: Optional[bool] = None
    topic: Optional[
        Dict[str, Union[Dict[str, Union[str, ImpactCategoryLabel]], str, None]]
    ] = None
    impact_category: Optional[ImpactCategoryLabel] = None
    query_id: Optional[str] = None
    query_string: str
    inference_settings: Optional[Dict[str, Any]] = None
