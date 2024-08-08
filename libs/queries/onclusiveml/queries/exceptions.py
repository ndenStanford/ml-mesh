"""Exceptions."""

# Internal libraries
from onclusiveml.core.base import OnclusiveException


class QueryESException(OnclusiveException):
    """Query exception."""

    message_format = "Failed to translate Boolean query to Elastic Search query."


class QueryPostException(OnclusiveException):
    """Media API POST method exception when trying to add boolean query."""

    message_format = (
        "Query could not be added to media api database database: {boolean_query}"
    )


class QueryMissingIdException(OnclusiveException):
    """Exception handling for when query id does not exist."""

    message_format = "Query id missing from response for boolean query: {boolean_query}"


class QueryGetException(OnclusiveException):
    """Media API GET method exception when trying to retrieve translated ES query with query id."""

    message_format = "Translated query  not found for the boolean query: {boolean_query}, queryId: {query_id}"  # noqa: E501


class QueryDeleteException(OnclusiveException):
    """Media API DELETE method exception when trying to delete query from database."""

    message_format = "Query could not be deleted for boolean query: {boolean_query}, queryId: {query_id}"  # noqa: E501


class QueryIdException(OnclusiveException):
    """Query id exception."""

    message_format = "Query not found for the query id: {query_id}"
