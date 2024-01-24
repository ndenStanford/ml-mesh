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
    GCH_SUMMARIZATION_TRAIN = "gch-summarization-train"
    GCH_SUMMARIZATION_SERVE = "gch-summarization-serve"

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

    # # --- topic
    TOPIC_REGISTER = "topic-register"
    TOPIC_TRAIN = "topic-train"
    TOPIC_SERVE = "topic-serve"

    # # --- IPTC
    IPTC_REGISTER = "iptc-register"
    IPTC_TRAIN = "iptc-train"
    IPTC_COMPILE = "iptc-compile"
    IPTC_SERVE = "iptc-serve"

    # APPS
    # --- summarization
    SUMMARIZATION_SERVE = "summarization-serve"
    TOPIC_SUMMARIZATION = "topic-summarization-serve"

    # --- prompt backend
    PROMPT_BACKEND_SERVE = "prompt-backend-serve"

    # --- Transcript Segmentation
    TRANSCRIPT_SEGMENTATION = "transcript-segmentation-serve"

    @classmethod
    def validate(cls, service: str) -> None:
        """Validates a service name against the internal service range.

        Args:
            service (str): Onlusive service name to be validated

        Raises:
            ValueError: If the `service` is not a value from the list of class attributes., this
                execption will be raised.
        """
        if service not in cls.list():
            raise ValueError(
                f"The specified service reference {service} is not in the valid range: "
                f"{OnclusiveService.list()}"
            )


class OnclusiveLogMessageFormat(OnclusiveEnum):
    """Standardized log message formats."""

    MESSAGE_ONLY = "%(message)s"
    BASIC = "%(levelname)s - %(message)s"
    SIMPLE = "%(asctime)s - %(levelname)s - %(message)s"
    DETAILED = "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"  # noqa: E501

    # requires OnclusiveFormatter (subclass) - meant for json log formatting
    DEFAULT = (
        "%(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"  # noqa: E501
    )
