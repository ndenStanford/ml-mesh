"""Prediction data schemas."""

# Internal libraries
from onclusiveml.core.serialization import JsonApiResponseSchema, JsonApiSchemas
from onclusiveml.serving.serialization.summarization.v2 import (
    BioRequestAttributeSchemaV2,
    PredictRequestAttributeSchemaV2,
    PredictRequestParametersSchemaV2,
    PredictResponseAttributeSchemaV2,
)

# Source
from src.settings import get_settings


settings = get_settings()


PredictRequestSchema, PredictResponseSchema = JsonApiSchemas(
    namespace=settings.model_name,
    request_attributes_schema=PredictRequestAttributeSchemaV2,
    response_attributes_schema=PredictResponseAttributeSchemaV2,
    request_parameters_schema=PredictRequestParametersSchemaV2,
)


BioResponseSchema = JsonApiResponseSchema(
    namespace=settings.model_name, attributes_schema=BioRequestAttributeSchemaV2
)
