"""Exceptions."""

# Internal libraries
from onclusiveml.core.base import OnclusiveException


class DataException(OnclusiveException):
    """Data exception."""

    message_format = "Unknown data lib error."


class QueryException(OnclusiveException):
    """Query exception."""

    message_format = "Query not found."


class QueryStringException(OnclusiveException):
    """Query string exception."""

    message_format = "Query not found for the boolean query: {boolean_query}"


class QueryIdException(OnclusiveException):
    """Query id exception."""

    message_format = "Query not found for the query id: {query_id}"
