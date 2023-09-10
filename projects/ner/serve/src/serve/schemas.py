"""Prediction data schemas."""

# Internal libraries
from onclusiveml.core.serialization import JsonApiResponseSchema, JsonApiSchemas
from onclusiveml.serving.serialization.ner.v1 import (
    BioRequestAttributeSchema,
    PredictRequestAttributeSchema,
    PredictRequestParametersSchema,
    PredictResponseAttributeSchema,
)

# Source
from src.settings import get_settings


settings = get_settings()


PredictRequestSchema, PredictResponseSchema = JsonApiSchemas(
    namespace=settings.model_name,
    request_attributes_schema=PredictRequestAttributeSchema,
    response_attributes_schema=PredictResponseAttributeSchema,
    request_parameters_schema=PredictRequestParametersSchema,
)


BioResponseSchema = JsonApiResponseSchema(
    namespace=settings.model_name, attributes_schema=BioRequestAttributeSchema
)
