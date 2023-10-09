# type: ignore
"""Response Schema."""

# Standard Library
from typing import Generic, Optional, Type, TypeVar

# 3rd party libraries
from pydantic.generics import GenericModel
from typing_extensions import Literal

# Internal libraries
from onclusiveml.core.serialization.schema import JsonApiSchema


NamespaceT = TypeVar("NamespaceT")
AttributesT = TypeVar("AttributesT")


class ResponseDataModel(GenericModel, Generic[NamespaceT, AttributesT]):
    """Response Data Model."""

    identifier: Optional[str] = None
    namespace: NamespaceT
    attributes: AttributesT


DataT = TypeVar("DataT", bound=ResponseDataModel)


class ResponseSchema(GenericModel, Generic[DataT]):
    """Response Schema."""

    version: int
    data: DataT

    @property
    def attributes(self) -> AttributesT:
        """Response attributes."""
        return self.data.attributes

    @classmethod
    def from_data(
        cls,
        namespace: str,
        version: int,
        attributes: AttributesT,
        identifier: Optional[str] = None,
    ) -> "ResponseSchema":
        """Instanciates schema from data (identifier, namespace and attributes)."""
        return cls(
            version=version,
            data={
                "identifier": identifier,
                "namespace": namespace,
                "attributes": attributes,
            },
        )


def JsonApiResponseSchema(
    namespace: str,
    attributes_schema: JsonApiSchema,
) -> Type[ResponseSchema]:
    """Json API Response schema."""
    response_data_model = ResponseDataModel[
        Literal[namespace],
        attributes_schema,
    ]
    response_model = ResponseSchema[response_data_model]
    return response_model
