"""Response test."""

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.core.serialization import JsonApiSchema
from onclusiveml.core.serialization.response import JsonApiResponseSchema


class TestResponseAttributesSchema(JsonApiSchema):
    """Test request attributes schema."""

    attr1: int
    attr2: int
    attr3: float


@pytest.mark.parametrize(
    "namespace, attr1, attr2, attr3, version",
    [("test", 1, 2999, 2.08, 1), ("t", 0, 100, 0.14, 3)],
)
def test_init_schema(namespace, attr1, attr2, attr3, version):
    """Test schema initialization."""
    ResponseSchema = JsonApiResponseSchema(
        namespace=namespace, attributes_schema=TestResponseAttributesSchema
    )

    response = ResponseSchema.from_data(
        namespace=namespace,
        attributes=TestResponseAttributesSchema(attr1=attr1, attr2=attr2, attr3=attr3),
        version=version,
    )

    assert response.namespace == namespace
    assert response.version == version
    assert response.attributes == TestResponseAttributesSchema(
        attr1=attr1, attr2=attr2, attr3=attr3
    )
