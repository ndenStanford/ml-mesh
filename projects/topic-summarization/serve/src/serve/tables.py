# isort: skip_file
"""Topic summarization table."""

# Standard Library
import uuid
from datetime import date, time
from typing import Dict, Optional, Union, List

# 3rd party libraries
from dyntastic import Dyntastic
from pydantic import Field
from decimal import Decimal

# Internal libraries
from onclusiveml.serving.serialization.topic_summarization.v1 import ImpactCategoryLabel

from src.serve.schema import (
    PredictResponseSchema,
)

# Source
from src.settings import get_settings

settings = get_settings()


class PredictResponseSchemaWID(PredictResponseSchema):
    """Extended PredictResponseSchema with an additional ID field.

    This class inherits from PredictResponseSchema and adds a unique
    identifier field 'id' to the schema.
    """

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))


class TopicSummaryResponseDB(Dyntastic, PredictResponseSchemaWID):
    """DynamoDB model for storing topic summary responses.

    This class combines Dyntastic for DynamoDB interactions and
    PredictResponseSchemaWID for the data structure. It defines
    the table configuration for storing topic summary responses.

    Attributes:
        __table_name__ (str): The name of the DynamoDB table.
        __hash_key__ (str): The primary key for the table.
        __table_region__ (str): The AWS region where the table is located.
        __table_host__ (str): The host address for the DynamoDB table.
    """


class TopicSummaryDynamoDB(Dyntastic):
    """Prediction request data."""

    __table_name__ = settings.DYNAMODB_TABLE_NAME
    __hash_key__ = "id"
    __table_region__ = "us-east-2"
    __table_host__ = settings.DYNAMODB_HOST

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp_date: date
    timestamp_time: time
    topic_id: int
    trending: Optional[bool] = None
    analysis: Optional[
        Dict[str, Union[Dict[str, Union[str, ImpactCategoryLabel]], str, List, None]]
    ] = None
    impact_category: Optional[ImpactCategoryLabel] = None
    query_id: Optional[str] = None
    query_string: Union[str, dict]
    trend_lookback_days: int
    topic_document_threshold: Decimal
    trend_time_interval: str
    days_past_inflection_point: int
    content: Optional[List[str]] = None
    query_all_doc_count: Optional[List[Dict[str, Union[str, int]]]] = None
    query_topic_doc_count: Optional[List[Dict[str, Union[str, int]]]] = None
    topic_summary_quality: Optional[bool] = None
