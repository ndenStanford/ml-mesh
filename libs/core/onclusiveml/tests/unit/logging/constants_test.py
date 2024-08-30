"""Constants tests."""

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.core.logging import OnclusiveService
from onclusiveml.core.logging.constants import LoggingLevel


def test_onclusive_service_validate_raise():
    """Tests the OnclusiveService.validate execption behaviour."""
    with pytest.raises(ValueError):
        OnclusiveService.from_value("invalid-service", raises_if_not_found=True)


@pytest.mark.parametrize(
    "service",
    [
        "onclusive-ml",
        "test-service",
        "entity-linking-serve",
        "gch-summarization-serve",
        "lsh-serve",
        "ner-train",
        "ner-compile",
        "ner-serve",
        "keywords-train",
        "keywords-compile",
        "keywords-serve",
        "sentiment-train",
        "sentiment-compile",
        "sentiment-serve",
        "summarization-serve",
        "topic-summarization-serve",
        "prompt-backend-serve",
    ],
)
def test_onclusive_service_validate(service):
    """Tests the OnclusiveService.validate validaton behaviour."""
    assert OnclusiveService.from_value(service, raises_if_not_found=True)


@pytest.mark.parametrize(
    "level, expected",
    [
        ("CRITICAL", 50),
        ("ERROR", 40),
        ("WARN", 30),
        ("INFO", 20),
        ("DEBUG", 10),
        ("NOTSET", 0),
    ],
)
def test_logging_level_conversion(level, expected):
    """Test logging level conversion logic."""
    log_level = LoggingLevel.from_name(level)

    assert log_level.value == expected
