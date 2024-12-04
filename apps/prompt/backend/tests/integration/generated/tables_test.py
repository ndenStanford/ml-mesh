"""Project routes test."""

# 3rd party libraries
import pytest

# Source
from src.generated.tables import Generated


@pytest.mark.parametrize(
    "data",
    [
        {
            "id": "e2977cc2-08ec-42bc-928a-c9e59c3fafe",
            "generation": {"generated": "generation-1"},
            "status": "PENDING",
            "model": "gpt-4o",
            "prompt": "english-summarization",
            "error": None,
            "model_parameters": {
                "temperature": "0.6",
            },
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
        status=data["status"],
        model=data["model"],
        prompt=data["prompt"],
        error=data["error"],
        model_parameters=data["model_parameters"],
        timestamp=data["timestamp"],
    )
    generated.save()
    Generated.get(data["id"])


@pytest.mark.parametrize("id", ["e2977cc2-08ec-42bc-928a-c9e59c3fafe"])
@pytest.mark.order(19)
def test_delete(id, app):
    """Test delete."""
    generated = Generated.get(id)
    generated.delete()
