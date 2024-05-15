"""Model test."""


# Source
from src.settings import get_settings


# from pytest_unordered import unordered


settings = get_settings()


def test_model_bio(summarization_served_model):
    """Model bio test."""
    assert summarization_served_model.bio().dict() == {
        "version": 1,
        "data": {
            "namespace": "summarization",
            "identifier": None,
            "attributes": {
                "model_name": "summarization",
                "model_card": {},
            },
        },
    }


def test_model_headers(summarization_served_model):
    """Test model headers."""
    assert summarization_served_model.headers == {"x-api-key": ""}
