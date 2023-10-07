"""Request schema."""

# Standard Library
from typing import Generic, Optional, Type, TypeVar

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

    identifier: Optional[str] = None
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

    @classmethod
    def from_data(
        cls,
        namespace: str,
        attributes: AttributesT,
        parameters: ParametersT,
        identifier: Optional[str] = None,
    ) -> "RequestSchema":
        """Instanciates schema from data (identifier, namespace, attributes and parameters)."""
        return cls(
            data={
                "identifier": identifier,
                "namespace": namespace,
                "attributes": attributes,
                "parameters": parameters,
            }
        )


def JsonApiRequestSchema(
    namespace: str, attributes_schema: JsonApiSchema, parameters_schema: JsonApiSchema
) -> Type[RequestSchema]:
    """JSON API Request.

    Args:
        namespace (str): namespace.
        attributes_schema (JsonApiSchema): attributes data schema.
        parameters_schema (JsonApiSchema): paramters data schema.
    """
    request_data_model = RequestDataModel[
        Literal[namespace], attributes_schema, parameters_schema
    ]
    # request_data_model.__name__ = f"RequestSchema[{namespace}]"
    request_model = RequestSchema[request_data_model]
    # request_model.__name__ = f"Request[{namespace}]"
    return request_model
