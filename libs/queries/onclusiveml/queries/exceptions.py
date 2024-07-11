"""Exceptions."""

# Internal libraries
from onclusiveml.core.base import OnclusiveException


class QueryESException(OnclusiveException):
    """Query exception."""

    message_format = "Failed to translate Boolean query to Elastic Search query."


class QueryStringException(OnclusiveException):
    """Query string exception."""

    message_format = "Query not found for the boolean query: {boolean_query}"


class QueryIdException(OnclusiveException):
    """Query id exception."""

    message_format = "Query not found for the query id: {query_id}"
