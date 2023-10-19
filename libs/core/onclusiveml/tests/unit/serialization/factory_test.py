"""Factory test."""

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.core.serialization import JsonApiSchema
from onclusiveml.core.serialization.factory import JsonApiSchemas


class TestRequestAttributesSchema(JsonApiSchema):
    """Test request attributes schema."""

    attr1: str
    attr2: float
    attr3: int


class TestRequestParametersSchema(JsonApiSchema):
    """Test request attributes schema."""

    param1: int


class TestResponseAttributesSchema(JsonApiSchema):
    """Test request attributes schema."""

    attr4: int
    attr5: int
    attr6: float


@pytest.mark.parametrize(
    "namespace, attr1, attr2, attr3, param1, version, attr4, attr5, attr6",
    [
        ("test", 1, 2999, 2.08, 1, 2, 100, 100, 0.1),
        ("t", 0, 100, 0.14, 3, 2, 63, 6, 9.3),
    ],
)
def test_init_schema(
    namespace, attr1, attr2, attr3, param1, version, attr4, attr5, attr6
):
    """Test schemas initialization."""
    RequestSchema, ResponseSchema = JsonApiSchemas(
        namespace=namespace,
        request_attributes_schema=TestRequestAttributesSchema,
        request_parameters_schema=TestRequestParametersSchema,
        response_attributes_schema=TestResponseAttributesSchema,
    )

    request = RequestSchema.from_data(
        namespace=namespace,
        attributes=TestRequestAttributesSchema(attr1=attr1, attr2=attr2, attr3=attr3),
        parameters=TestRequestParametersSchema(param1=param1),
    )

    response = ResponseSchema.from_data(
        namespace=namespace,
        attributes=TestResponseAttributesSchema(attr4=attr4, attr5=attr5, attr6=attr6),
        version=version,
    )

    assert request.identifier is None
    assert request.namespace == namespace
    assert request.attributes == TestRequestAttributesSchema(
        attr1=attr1, attr2=attr2, attr3=attr3
    )
    assert request.parameters == TestRequestParametersSchema(param1=param1)

    assert response.namespace == namespace
    assert response.version == version
    assert response.attributes == TestResponseAttributesSchema(
        attr4=attr4, attr5=attr5, attr6=attr6
    )
