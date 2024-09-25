"""Constants."""

# Standard Library
import logging

# Internal libraries
from onclusiveml.core.base import OnclusiveEnum, OnclusiveStrEnum


DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL


LOG_LEVELS = (DEBUG, INFO, WARNING, ERROR, CRITICAL)


class LoggingLevel(OnclusiveEnum):
    """Enum for logging levels."""

    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR
    WARN = logging.WARN
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    NOTSET = logging.NOTSET


class OnclusiveService(OnclusiveStrEnum):
    """Standardized onclusive ML app and project service references for JSON logging."""

    DEFAULT = "onclusive-ml"
    TEST = "test-service"
    # PROJECTS
    # --- entity linking
    ENTITY_LINKING = "entity-linking-serve"
    # --- gch summarization
    GCH_SUMMARIZATION_TRAIN = "gch-summarization-train"
    GCH_SUMMARIZATION_SERVE = "gch-summarization-serve"
    # --- lsh
    LSH = "lsh-serve"
    # --- translation
    TRANSLATION = "translation-serve"
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
    # # --- topic
    TOPIC_REGISTER = "topic-register"
    TOPIC_TRAIN = "topic-train"
    TOPIC_SERVE = "topic-serve"
    # # --- IPTC
    IPTC_REGISTER = "iptc-register"
    IPTC_TRAIN = "iptc-train"
    IPTC_COMPILE = "iptc-compile"
    IPTC_SERVE = "iptc-serve"
    IPTC_MULTI_CLIENT = "iptc-multi-client"
    # APPS
    # --- summarization
    SUMMARIZATION_SERVE = "summarization-serve"
    TOPIC_SUMMARIZATION = "topic-summarization-serve"
    # --- prompt backend
    PROMPT_BACKEND_SERVE = "prompt-backend-serve"
    # --- Transcript Segmentation
    TRANSCRIPT_SEGMENTATION = "transcript-segmentation-serve"
    # --- Visitor Estimation
    VISITOR_ESTIMATION = "visitor-estimation-register"


class OnclusiveLogMessageFormat(OnclusiveStrEnum):
    """Standardized log message formats."""

    MESSAGE_ONLY = "%(message)s"
    BASIC = "%(levelname)s - %(message)s"
    SIMPLE = "%(asctime)s - %(levelname)s - %(message)s"
    DETAILED = "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"  # noqa: E501
    # requires OnclusiveFormatter (subclass) - meant for json log formatting
    DEFAULT = (
        "%(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"  # noqa: E501
    )
