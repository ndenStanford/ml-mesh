"""Exceptions."""

# Internal libraries
from onclusiveml.core.base import OnclusiveException


class DataModelException(OnclusiveException):
    """Exception raised for general data model errors."""

    message_format = "Data model error: {error}"


class ItemNotFoundException(OnclusiveException):
    """Exception raised when an item is not found."""

    message_format = "Item with id {item_id} does not exist."


class QueryNotFoundException(OnclusiveException):
    """Exception raised when an query is not found."""

    message_format = "Query {search_query}"


class ValidationException(OnclusiveException):
    """Exception raised for validation errors."""

    message_format = "Validation error: {error}"
