"""Table tests."""

# Standard Library
from unittest.mock import patch

# 3rd party libraries
import pytest
from dyntastic import Dyntastic

# Source
from src.generated.exceptions import GeneratedInvalidId
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
def test_valid_id(data):
    """Test valid id."""
    _ = Generated(**data)


@pytest.mark.parametrize(
    "data",
    [
        {
            "id": "e2977cc2-08ec-42bc-928a-c9e59c3fafe&*",
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
def test_invalid_id(data):
    """Test valid id."""
    with pytest.raises(GeneratedInvalidId):
        _ = Generated(**data)


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
@patch.object(Dyntastic, "save")
def test_save(mock_dyntastic_save, data):
    """Test save."""
    # call
    generated = Generated(**data)
    generated.save()
    # asserts
    mock_dyntastic_save.assert_called_once()


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
@patch.object(Dyntastic, "delete")
def test_delete(mock_dyntastic_delete, data):
    """Test delete."""
    # call
    generated = Generated(**data)
    generated.delete()
    # asserts
    mock_dyntastic_delete.assert_called_once()
