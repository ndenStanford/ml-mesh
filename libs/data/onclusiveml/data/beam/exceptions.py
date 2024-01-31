"""Exceptions."""

# Internal libraries
from onclusiveml.data.exceptions import DataException


class BeamPipelineException(DataException):
    """Enrichment pipeline exception."""

    message_format = "Unknown error thrown while running a beam pipeline."


class KafkaProducerException(BeamPipelineException):
    """Exception raised by kakfa producer."""

    message_format = "Error while submitting message to kakfa topic: {topic}."


class KafkaConsumerException(BeamPipelineException):
    """Exception raised by kakfa comsumer."""

    message_format = "Error while polling kakfa topic: {topic}. Message: {message}"


class EmptyConsumerException(BeamPipelineException):
    """Exception raised by kakfa consumer."""

    message_format = "No message in topics: {topics}."
