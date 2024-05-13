"""Topic summarization table."""

import uuid
from typing import Any, Dict, Optional, Union

from dyntastic import Dyntastic
from onclusiveml.serving.serialization.topic_summarization.v1 import ImpactCategoryLabel
from pydantic import BaseModel, Field

# Source
from src.settings import get_settings

settings = get_settings()


class CustomBaseModel(BaseModel):
    """Custom data."""

    @classmethod
    def custom_field(cls, default: Any = None, **kwargs) -> Field:
        """Convert None to N/A."""
        return Field(default=default if default is not None else "N/A", **kwargs)


class TopicSummaryDynamoDB(Dyntastic):
    """Prediction request data."""

    __table_name__ = "topic_summary"
    __hash_key__ = "query_id"
    __table_region__ = settings.AWS_DEFAULT_REGION
    __table_host__ = settings.DYNAMODB_HOST

    topic_summary_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    topic: Optional[
        Dict[str, Optional[Union[str, Dict[str, str]]]]
    ] = CustomBaseModel.custom_field()
    impact_category: Optional[ImpactCategoryLabel] = CustomBaseModel.custom_field()
    query_id: Optional[str] = CustomBaseModel.custom_field()
    query_string: str
