"""Topic Summarization v1 data schemas."""

# Standard Library
from datetime import datetime
from typing import List, Optional

# Internal libraries
from onclusiveml.core.base import OnclusiveEnum
from onclusiveml.core.serialization import JsonApiSchema


class PredictRequestAttributeSchemaV1(JsonApiSchema):
    """Prediction request data."""

    content: Optional[List[str]] = None
    topic_id: Optional[int] = None
    query_string: Optional[str] = None
    trend_detection: Optional[bool] = True
    query_id: Optional[str] = None
    media_api_version: Optional[str] = "1"
    save_report_dynamodb: bool = False
    media_api_query: Optional[str] = None


class PredictRequestParametersSchemaV1(JsonApiSchema):
    """Prediction request parameter data."""

    override_topic_document_threshold: Optional[float] = None
    override_trend_time_interval: Optional[str] = None
    override_trend_lookback_days: Optional[int] = None
    override_document_collector_end_date: Optional[int] = None
    """Prediction request paramaters data."""


class ImpactCategoryLabel(str, OnclusiveEnum):
    """Impact category label."""

    LOW = "low"
    MID = "mid"
    HIGH = "high"


class Analysis(JsonApiSchema):
    """Analysis of each topic."""

    summary: Optional[str] = None
    theme: Optional[str] = None
    impact: Optional[ImpactCategoryLabel] = None
    sources: Optional[str] = None


class Topic(JsonApiSchema):
    """Topic analysis schema."""

    opportunities: Analysis = Analysis()
    risk: Analysis = Analysis()
    threats: Analysis = Analysis()
    company: Analysis = Analysis()
    brand: Analysis = Analysis()
    ceo: Analysis = Analysis()
    customer: Analysis = Analysis()
    stock: Analysis = Analysis()
    industry: Analysis = Analysis()
    environment: Analysis = Analysis()
    summary: str
    theme: str


class PredictResponseAttributeSchemaV1(JsonApiSchema):
    """Prediction request data."""

    topic: Optional[Topic] = None
    impact_category: Optional[ImpactCategoryLabel]
    trending: Optional[bool] = None
    timestamp: datetime
    topic_summary_quality: Optional[bool] = None


class BioRequestAttributeSchemaV1(JsonApiSchema):
    """Response model for a bio response.

    Attributes:
        model_name (str): The name of the model used for prediction
        model_card (Dict): Information about the model
    """

    model_name: str = "topic-summarization"
