"""Exceptions."""

# Internal libraries
from onclusiveml.core.base.exception import OnclusiveException


class OnclusiveMachineLearningAPIError(OnclusiveException):
    """API exception."""

    message_format = (
        "API error code={code} was encountered while executing this request!"
    )
