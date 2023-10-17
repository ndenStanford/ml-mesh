"""Constants."""

# Standard Library
import logging
import sys

# Internal libraries
from onclusiveml.core.base.utils import OnclusiveEnum


DEFAULT_LOGGING_HANDLER: logging.Handler = logging.StreamHandler(sys.stdout)

DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

VALID_LOG_LEVELS = (DEBUG, INFO, WARNING, ERROR, CRITICAL)


class OnclusiveLogMessageFormats(OnclusiveEnum):
    """Standardized log message formats."""

    MESSAGE_ONLY = "%(message)s"
    BASIC = "%(levelname)s - %(message)s"
    SIMPLE = "%(asctime)s - %(levelname)s - %(message)s"
    DETAILED = "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"  # noqa: E501
