"""JsonApiResponse factory."""

# Standard Library
from typing import Tuple

# Internal libraries
from onclusiveml.core.serialization.request import (
    JsonApiRequestSchema,
    RequestSchema,
)
from onclusiveml.core.serialization.response import (
    JsonApiResponseSchema,
    ResponseSchema,
)
from onclusiveml.core.serialization.schema import JsonApiSchema


def JsonApiSchemas(
    namespace: str,
    request_attributes_schema: JsonApiSchema,
    request_parameters_schema: JsonApiSchema,
    response_attributes_schema: JsonApiSchema,
) -> Tuple[RequestSchema, ResponseSchema]:
    """Instanciates JSON API model input / output from specific API schemas.

    Args:
        namespace (str): namespace.
        request_attributes_schema (JsonApiSchema): request attributes schema.
        request_parameters_schema (JsonApiSchema): request parameters schema.
        response_attributes_schema (JsonApiSchema): response attributes schema.
    """
    return (
        JsonApiRequestSchema(
            namespace, request_attributes_schema, request_parameters_schema
        ),
        JsonApiResponseSchema(namespace, response_attributes_schema),
    )
