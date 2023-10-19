"""Request test."""

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.core.serialization import JsonApiSchema
from onclusiveml.core.serialization.request import JsonApiRequestSchema


class TestRequestAttributesSchema(JsonApiSchema):
    """Test request attributes schema."""

    attr1: str
    attr2: float
    attr3: int


class TestRequestParametersSchema(JsonApiSchema):
    """Test request attributes schema."""

    param1: int


@pytest.mark.parametrize(
    "namespace, attr1, attr2, attr3, param1",
    [("test", "aaa", 1.1, 2999, 1), ("t", "ddda", -0.3, 100, 0)],
)
def test_init_schema(namespace, attr1, attr2, attr3, param1):
    """Test schema initialization."""
    RequestSchema = JsonApiRequestSchema(
        namespace=namespace,
        attributes_schema=TestRequestAttributesSchema,
        parameters_schema=TestRequestParametersSchema,
    )

    request = RequestSchema.from_data(
        namespace=namespace,
        attributes=TestRequestAttributesSchema(attr1=attr1, attr2=attr2, attr3=attr3),
        parameters=TestRequestParametersSchema(param1=param1),
    )

    assert request.identifier is None
    assert request.namespace == namespace
    assert request.attributes == TestRequestAttributesSchema(
        attr1=attr1, attr2=attr2, attr3=attr3
    )
    assert request.parameters == TestRequestParametersSchema(param1=param1)
