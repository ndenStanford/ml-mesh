"""Request schema."""

# Standard Library
from typing import Any, Generic, List, Optional, Type, TypeVar

# 3rd party libraries
from pydantic.generics import GenericModel
from typing_extensions import Literal

# Internal libraries
from onclusiveml.core.serialization.schema import JsonApiSchema


NamespaceT = TypeVar("NamespaceT")
AttributesT = TypeVar("AttributesT")
ParametersT = TypeVar("ParametersT")


class RequestDataModel(GenericModel, Generic[NamespaceT, AttributesT, ParametersT]):
    """Request Data Model."""

    id: Optional[str]
    namespace: NamespaceT
    attributes: AttributesT
    parameters: ParametersT


DataT = TypeVar("DataT", bound=RequestDataModel)


class RequestSchema(GenericModel, Generic[DataT]):
    """Request Schema."""

    data: DataT

    @property
    def attributes(self) -> AttributesT:
        """Request attributes."""
        return self.data.attributes

    @property
    def parameters(self) -> ParametersT:
        """Parameters attributes."""
        return self.data.parameters


def JsonApiRequestSchema(
    namespace: str, attributes_model: JsonApiSchema, parameters_model: JsonApiSchema
) -> Type[RequestSchema]:
    """JSON API Request.
    Args:
        namespace (str):
        attributes_model (JsonApiSchema):
        parameters_model (JsonApiSchema):
    """
    request_data_model = RequestDataModel[
        Literal[namespace], attributes_model, parameters_model
    ]
    request_data_model.__name__ = f"RequestSchema[{namespace}]"
    request_model = RequestSchema[request_data_model]
    request_model.__name__ = f"Request[{namespace}]"
    return request_model
