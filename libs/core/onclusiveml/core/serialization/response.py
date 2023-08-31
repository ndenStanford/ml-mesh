"""Response Schema."""

# Standard Library
from typing import Any, Generic, List, Optional, Type, TypeVar, get_type_hints

# 3rd party libraries
from pydantic.generics import GenericModel
from typing_extensions import Literal

# Internal libraries
from onclusiveml.core.serialization.schema import JsonApiSchema


NamespaceT = TypeVar("NamespaceT")
AttributesT = TypeVar("AttributesT")


class ResponseDataModel(GenericModel, Generic[NamespaceT, AttributesT]):
    """Response Data Model."""

    id: Optional[str]
    namespace: NamespaceT
    attributes: AttributesT


DataT = TypeVar("DataT", bound=ResponseDataModel)


class ResponseSchema(GenericModel, Generic[DataT]):
    """Response Schema."""

    data: DataT

    @property
    def attributes(self) -> AttributesT:
        """Response attributes."""
        return self.data.attributes


def JsonApiResponseSchema(
    type_string: str,
    attributes_model: JsonApiSchema,
) -> Type[ResponseSchema]:
    """Json API Response schema."""
    response_data_model = ResponseDataModel[
        Literal[type_string],
        attributes_model,
    ]
    response_data_model.__name__ = f"ResponseSchema[{type_string}]"
    response_model = ResponseSchema[response_data_model]
    response_model.__name__ = f"Response[{type_string}]"
    return response_model
