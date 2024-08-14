"""Base Exception."""

# Internal libraries
from onclusiveml.core.base.exception import OnclusiveException


class TopicSummaryInsertionException(OnclusiveException):
    """Topic summary insertion exception."""

    message_format = (
        "Insertion error for topic summary dict: {dynamodb_dict} with error {e}"
    )


class TopicSummarizationParsingException(OnclusiveException):
    """Exception for output parsing error in topic summarization."""

    message_format = "Output parsing error occurred in topic summarization: '{e}'"


class TopicSummarizationJSONDecodeException(OnclusiveException):
    """Exception for Json decoding error in topic summarization."""

    message_format = "Json decoding error occurred in topic summarization: '{e}'"
