"""Init."""

# Internal libraries
from onclusiveml.serving.rest.crud.dynamodb_router import (  # noqa: F401
    DynamoDBCRUDRouter,
)


__all__ = [
    "DynamoDBCRUDRouter",
]
