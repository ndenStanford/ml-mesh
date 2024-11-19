"""Project routes test."""

# 3rd party libraries
import pytest

# Source
from src.generated.tables import Generated


@pytest.mark.parametrize(
    "data",
    [
        {
            "id": "e2478dc2-08ec-42bc-928a-c9e59c3fafe",
            "generation": "test1",
            "method": "src.prompt.functional.generate_from_prompt_template",
            "args": ["english-summarization", "gpt-4o"],
            "kwargs": {"input": {"number": 5, "text": "What is the capital of US?"}},
            "timestamp": "2024-11-19T12:00:00",
        }
    ],
)
@pytest.mark.order(18)
def test_save(data, app):
    """Test save."""
    generated = Generated(
        id=data["id"],
        generation=data["generation"],
        method=data["generation"],
        args=data["args"],
        kwargs=data["kwargs"],
        timestamp=data["timestamp"],
    )
    generated.save()
    Generated.safe_get(data["id"])


@pytest.mark.parametrize("id", ["e2478dc2-08ec-42bc-928a-c9e59c3fafe"])
@pytest.mark.order(19)
def test_delete(id, app):
    """Test delete."""
    generated = Generated.get(id)
    generated.delete()
    assert Generated.safe_get(id) is None
