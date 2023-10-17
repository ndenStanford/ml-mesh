"""Constants."""

# Standard Library
import logging

# Internal libraries
from onclusiveml.core.base.utils import OnclusiveEnum


DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

VALID_LOG_LEVELS = (DEBUG, INFO, WARNING, ERROR, CRITICAL)


class OnclusiveLogMessageFormat(OnclusiveEnum):
    """Standardized log message formats."""

    MESSAGE_ONLY = "%(message)s"
    BASIC = "%(levelname)s - %(message)s"
    SIMPLE = "%(asctime)s - %(levelname)s - %(message)s"
    DETAILED = "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"  # noqa: E501
