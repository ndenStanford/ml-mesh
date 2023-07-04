# Internal libraries
from onclusiveml.core.base.exception import OnclusiveException


class StopwordsFileException(OnclusiveException):
    message_format = "No stopword file found for {language}"
