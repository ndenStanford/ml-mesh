"""Routes tests."""

# Standard Library
from unittest.mock import patch

# 3rd party libraries
import pytest
from fastapi import status

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
@patch.object(Generated, "save")
@patch.object(Generated, "get")
def test_create_generated(
    mock_generated_get, mock_generated_save, data, test_client
):
    """Test save generated endpoint."""
    # setup
    mock_generated_get.return_value = None
    # mock call
    response = test_client.post(
        "/api/v3/generated", headers={"x-api-key": "1234"}, json=data
    )
    # asserts
    assert response.status_code == status.HTTP_201_CREATED
    mock_generated_save.assert_called_once()


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
@patch.object(Generated, "delete")
@patch.object(Generated, "get")
def test_delete_generated(mock_generated_get, mock_generated_delete, data, test_client):
    """Test generated delete endpoint."""
    mock_generated_get.return_value = Generated(**data)

    response = test_client.delete(
        f"/api/v3/generated/{data['id']}", headers={"x-api-key": "1234"}
    )

    assert response.status_code == status.HTTP_200_OK
    mock_generated_delete.assert_called_once()
    mock_generated_get.assert_called_with(data["id"])


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
@patch.object(Generated, "get")
def test_get_generated(mock_generated_get, data, test_client):
    """Test get generated endpoint."""
    # setup
    mock_generated_get.return_value = Generated(**data)
    # call
    response = test_client.get(f"/api/v3/generated/{id}", headers={"x-api-key": "1234"})
    # asserts
    assert response.status_code == status.HTTP_200_OK
    response.json() == Generated(**data)
