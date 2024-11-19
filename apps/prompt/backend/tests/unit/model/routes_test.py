"""Test routes."""

# Standard Library
from types import SimpleNamespace
from unittest.mock import patch

# 3rd party libraries
import pytest
from fastapi import status

# Source
from src.model.tables import LanguageModel
from src.settings import get_settings


settings = get_settings()


@patch.object(LanguageModel, "scan")
def test_get_models(mock_model_get, test_client):
    """Test get models endpoint."""
    mock_model_get.return_value = []
    response = test_client.get("/api/v3/models", headers={"x-api-key": "1234"})
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
    """Test get model endpoint."""
    mock_model_get.return_value = LanguageModel(alias=alias, provider=provider)
    response = test_client.get(f"/api/v3/models/{alias}", headers={"x-api-key": "1234"})
    mock_model_get.assert_called_with(f"{alias}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "alias": alias,
        "model_parameters": None,
        "provider": provider,
    }


@pytest.mark.parametrize(
    "alias, provider, prompt",
    [
        ("model-1", "openai", "test prompt"),
        ("model-2", "bedrock", "hello"),
    ],
)
@patch("src.prompt.functional.generate_from_prompt.delay")
def test_generate(mock_generate, alias, provider, prompt, test_client):
    """Test get model endpoint."""
    mock_generate.return_value = SimpleNamespace(**{"id": "1234"})
    response = test_client.post(
        f"/api/v3/models/{alias}/generate?prompt={prompt}",
        headers={"x-api-key": "1234"},
    )
    mock_generate.assert_called_with(prompt, alias, model_parameters=None)
    assert response.status_code == status.HTTP_200_OK
