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


class OnclusiveService(OnclusiveEnum):
    """Standardized onclusive ML app and project service references for JSON logging."""

    DEFAULT = "onclusive-ml"
    TEST = "test-service"

    # PROJECTS
    # --- entity linking
    ENTITY_LINKING = "entity-linking-serve"

    # --- gch summarization
    GCH_SUMMARIZATION = "gch-summarization-serve"

    # --- lsh
    LSH = "lsh-serve"

    # --- ner
    NER_TRAIN = "ner-train"
    NER_COMPILE = "ner-compile"
    NER = "ner-serve"

    # --- keywords
    KEYWORDS_TRAIN = "keywords-train"
    KEYWORDS_COMPILE = "keywords-compile"
    KEYWORDS_SERVE = "keywords-serve"

    # # --- sentiment
    SENTIMENT_TRAIN = "sentiment-train"
    SENTIMENT_COMPILE = "sentiment-compile"
    SENTIMENT_SERVE = "sentiment-serve"

    # APPS
    # --- summarization
    SUMMARIZATION_SERVE = "summarization-serve"

    # --- prompt backend
    PROMPT_BACKEND_SERVE = "prompt-backend-serve"


class OnclusiveLogMessageFormat(OnclusiveEnum):
    """Standardized log message formats."""

    MESSAGE_ONLY = "%(message)s"
    BASIC = "%(levelname)s - %(message)s"
    SIMPLE = "%(asctime)s - %(levelname)s - %(message)s"
    DETAILED = "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"  # noqa: E501

    # requires OnclusiveJSONFormatter (subclass)
    JSON = "%(service)s | %(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"  # noqa: E501
