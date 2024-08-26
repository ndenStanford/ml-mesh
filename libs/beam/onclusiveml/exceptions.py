"""Exceptions."""

# Internal libraries
from onclusiveml.core.base import OnclusiveException


class DataException(OnclusiveException):
    """Data exception."""

    message_format = "Unknown data lib error."
