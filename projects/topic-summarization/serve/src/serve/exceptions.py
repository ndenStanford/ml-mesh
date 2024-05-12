"""Base Exception."""

# Internal libraries
from onclusiveml.core.base.exception import OnclusiveException


class TopicSummaryInsertionException(OnclusiveException):
    """Topic summary insertion exception."""

    message_format = "Insertion error for query string: {query_string}"
