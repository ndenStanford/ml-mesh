"""Test routes."""

# Standard Library
import json
from unittest.mock import patch

# 3rd party libraries
import pytest
from fastapi import status

# Source
from src.model.tables import LanguageModel
from src.settings import get_settings


settings = get_settings()


def test_health_route(test_client):
    """Test health endpoint."""
    response = test_client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == "OK"


@patch.object(LanguageModel, "scan")
def test_get_models(mock_model_get, test_client):
    """Test get models endpoint."""
    mock_model_get.return_value = []
    response = test_client.get("/api/v2/models", headers={"x-api-key": "1234"})
    mock_model_get.assert_called_once()
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.parametrize(
    "alias, provider",
    [
        ("model-1", "openai"),
        ("model-2", "openai"),
        ("model-3", "bedrock"),
    ],
)
@patch.object(LanguageModel, "get")
def test_get_model(mock_model_get, alias, provider, test_client):
    """Test get model."""
    """Test get model endpoint."""
    mock_model_get.return_value = LanguageModel(alias=alias, prodiver=provider)
    response = test_client.get(f"/api/v2/models/{alias}", headers={"x-api-key": "1234"})
    raises_if_not_found = True
    mock_model_get.assert_called_with(
        f"{model_name}", raises_if_not_found=raises_if_not_found
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "created_at": None,
        "id": "123abc",
        "model_name": model_name,
        "parameters": parameters,
    }
