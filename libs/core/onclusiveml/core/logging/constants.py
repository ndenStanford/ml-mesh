"""Constants."""

# Standard Library
import logging
import sys
from enum import Enum


DEFAULT_LOGGING_HANDLER: logging.Handler = logging.StreamHandler(sys.stdout)


class LogFormat(Enum):
    """Standardized logging formats."""

    MESSAGE_ONLY = "%(message)s"
    BASIC = "%(levelname)s - %(message)s"
    SIMPLE = "%(asctime)s - %(levelname)s - %(message)s"
    DETAILED = "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"  # noqa: E501
