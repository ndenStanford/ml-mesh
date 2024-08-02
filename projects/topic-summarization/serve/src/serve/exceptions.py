"""Base Exception."""

# Internal libraries
from onclusiveml.core.base.exception import OnclusiveException


class TopicSummaryInsertionException(OnclusiveException):
    """Topic summary insertion exception."""

    message_format = (
        "Insertion error for topic summary dict: {dynamodb_dict} with error {e}"
    )


class TopicSummarizationParsingException(OnclusiveException):
    """Exception for errors in topic summarization parsing."""

    message_format = "Error occurred in topic summarization parsing: '{e}'"
