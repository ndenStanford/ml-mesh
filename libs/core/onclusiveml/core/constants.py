"""Constants."""

import logging
import sys
from enum import Enum


class LogFormat(Enum):
    """Standardized logging formats."""

    SIMPLE = "%(asctime)s - %(levelname)s - %(message)s"
    DETAILED = "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"  # noqa: E501


DEFAULT_LOGGING_HANDLER = logging.StreamHandler(sys.stdout)
