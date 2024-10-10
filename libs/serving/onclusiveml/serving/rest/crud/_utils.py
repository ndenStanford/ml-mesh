"""Utilities."""

# Standard Library
from typing import Any, Dict, Optional, Type, TypeVar

# 3rd party libraries
from fastapi import Depends, HTTPException
from pydantic import BaseModel, create_model


T = TypeVar("T", bound=BaseModel)


class AttrDict(dict):  # type: ignore
    """Dictionary subclass that allows access to its keys as attributes."""

    def __init__(self, *args, **kwargs) -> None:  # type: ignore
        """Initialize the AttrDict instance.

        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def get_pk_type(schema: Type[BaseModel], pk_field: str) -> Any:
    """Retrieve the type of the primary key field from a Pydantic schema.

    Args:
        schema (Type[BaseModel]): The Pydantic model class
        pk_field (str): The name of the primary key field
    Returns:
        Any: The type of the primary key field, or int if the field is not found
    """
    try:
        return schema.__fields__[pk_field].type_
    except KeyError:
        return int


def schema_factory(
    schema_cls: Type[T], pk_field_name: str = "id", name: str = "Create"
) -> Type[T]:
    """Create a new Pydantic model excluding the primary key field.

    Useful for generating schemas for create operations where PK is not provided by client
    Args:
        schema_cls (Type[T]): The original Pydantic model class
        pk_field_name (str, optional): The name of the primary key field to exclude
        name (str, optional): The suffix to add to the new model's name
    Returns:
        Type[T]: A new Pydantic model class without the primary key field
    """
    fields = {
        f.name: (f.type_, ...)
        for f in schema_cls.__fields__.values()
        if f.name != pk_field_name
    }

    name = schema_cls.__name__ + name
    schema: Type[T] = create_model(__model_name=name, **fields)  # type: ignore
    return schema


def create_query_validation_exception(field: str, msg: str) -> HTTPException:
    """Create an HTTPException for query parameter validation errors.

    Args:
        field (str): The name of the query parameter that caused the error
        msg (str): The error message
    Returns:
        HTTPException: An HTTPException with a detailed error message
    """
    return HTTPException(
        422,
        detail={
            "detail": [
                {"loc": ["query", field], "msg": msg, "type": "type_error.integer"}
            ]
        },
    )


def pagination_factory(max_limit: Optional[int] = None) -> Any:
    """Create a pagination dependency for FastAPI routes.

    Args:
        max_limit (Optional[int], optional): The maximum allowed value for the limit parameter
    Returns:
        Any: A FastAPI dependency that handles pagination parameters
    """

    def pagination(
        skip: int = 0, limit: Optional[int] = max_limit
    ) -> Dict[str, Optional[int]]:
        """Validate and return pagination parameters.

        Args:
            skip (int, optional): The number of items to skip
            limit (Optional[int], optional): The maximum number of items to return
        Raises:
            HTTPException: If skip or limit parameters are invalid
        Returns:
            Dict[str, Optional[int]]: Dict containing the validated skip and limit parameters
        """
        if skip < 0:
            raise create_query_validation_exception(
                field="skip",
                msg="skip query parameter must be greater or equal to zero",
            )

        if limit is not None:
            if limit <= 0:
                raise create_query_validation_exception(
                    field="limit", msg="limit query parameter must be greater than zero"
                )

            elif max_limit and max_limit < limit:
                raise create_query_validation_exception(
                    field="limit",
                    msg=f"limit query parameter must be less than {max_limit}",
                )

        return {"skip": skip, "limit": limit}

    return Depends(pagination)
