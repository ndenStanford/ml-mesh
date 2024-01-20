"""Prediction data schemas."""
# isort: skip_file

# Internal libraries
from onclusiveml.core.serialization import JsonApiResponseSchema, JsonApiSchemas
from onclusiveml.serving.serialization.topic_summarization.v1 import (
    BioRequestAttributeSchemaV1,
    PredictRequestAttributeSchemaV1,
    PredictRequestParametersSchemaV1,
    PredictResponseAttributeSchemaV1,
)

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
