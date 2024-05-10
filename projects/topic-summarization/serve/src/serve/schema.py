"""Prediction data schemas."""
# isort: skip_file

from typing import Optional, Dict, Union

# Internal libraries
from onclusiveml.core.serialization import JsonApiResponseSchema, JsonApiSchemas
from onclusiveml.serving.serialization.topic_summarization.v1 import (
    BioRequestAttributeSchemaV1,
    PredictRequestAttributeSchemaV1,
    PredictRequestParametersSchemaV1,
    PredictResponseAttributeSchemaV1,
)
from dyntastic import Dyntastic
from onclusiveml.serving.serialization.topic_summarization.v1 import ImpactCategoryLabel

# Source
from src.settings import get_settings

settings = get_settings()


PredictRequestSchema, PredictResponseSchema = JsonApiSchemas(
    namespace=settings.model_name,
    request_attributes_schema=PredictRequestAttributeSchemaV1,
    response_attributes_schema=PredictResponseAttributeSchemaV1,
    request_parameters_schema=PredictRequestParametersSchemaV1,
)


BioResponseSchema = JsonApiResponseSchema(
    namespace=settings.model_name, attributes_schema=BioRequestAttributeSchemaV1
)


class TopicSummaryDynamoDB(Dyntastic):
    """Prediction request data."""

    __table_name__ = "model"
    __hash_key__ = "alias"
    __table_region__ = settings.AWS_DEFAULT_REGION
    __table_host__ = settings.DYNAMODB_HOST

    topic: Optional[Dict[str, Optional[Union[str, Dict[str, str]]]]]
    impact_category: Optional[ImpactCategoryLabel]
