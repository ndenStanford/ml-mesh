"""Test routes.x"""

# Standard Library
import json
from unittest.mock import patch

# 3rd party libraries
import pytest
from fastapi import status

# Source
from src.model.schemas import ModelSchema
from src.settings import get_settings


def test_health_route(test_client):
    """Test health endpoint."""
    response = test_client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == "OK"


@patch.object(ModelSchema, "get")
def test_get_models(mock_model_get, test_client):
    """Test get models endpoint."""
    mock_model_get.return_value = []
    response = test_client.get("/api/v1/models", headers={"x-api-key": "1234"})
    mock_model_get.assert_called_once()
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"models": []}


def test_get_models_unauthenticated(test_client):
    """Test get models endpoint unauthenticated."""
    response = test_client.get("/api/v1/models")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "Not authenticated"}


@pytest.mark.parametrize("id", [1, 124543, "2423"])
@patch.object(ModelSchema, "get")
def test_get_model(mock_model_get, id, test_client):
    settings = get_settings()
    """Test get model endpoint."""
    mock_model_get.return_value = ModelSchema(id=id, model_name="test-model")
    response = test_client.get(f"/api/v1/models/{id}", headers={"x-api-key": "1234"})
    mock_model_get.assert_called_with(f"{id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "created_at": None,
        "id": f"{id}",
        "model_name": "test-model",
        "parameters": json.dumps(
            {
                "max_tokens": settings.OPENAI_MAX_TOKENS,
                "temperature": settings.OPENAI_TEMPERATURE,
            }
        ),
    }


def test_get_model_unauthenticated(test_client):
    """Test get model endpoint unauthenticated."""
    response = test_client.get("/api/v1/models/1")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "Not authenticated"}
