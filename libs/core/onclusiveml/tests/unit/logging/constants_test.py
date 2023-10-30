"""Constants tests."""
# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.core.logging import OnclusiveService


def test_onclusive_service_validate_raise():
    """Tests the OnclusiveService.validate execption behaviour."""
    with pytest.raises(ValueError):
        OnclusiveService.validate("invalid-service")


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
        "prompt-backend-serve",
    ],
)
def test_onclusive_service_validate(service):
    """Tests the OnclusiveService.validate validaton behaviour."""
    OnclusiveService.validate(service)
