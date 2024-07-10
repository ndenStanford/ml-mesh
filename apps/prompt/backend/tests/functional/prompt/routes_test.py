"""Prompt namespace tests."""

# 3rd party libraries
import pytest
import requests


@pytest.mark.parametrize(
    "model_parameters",
    [
        '{"temperature": 0.5, "maxTokens": 3000}',
        '{"temperature": 0.7, "maxTokens": 1500}',
        '{"temperature": 1.0, "maxTokens": 1000}',
    ],
)
def test_server_response_status_code(
    url_prompt_namespace, headers, payload, model_parameters
):
    """Test server response code."""
    headers["model-parameters"] = model_parameters
    response = requests.post(url_prompt_namespace, json=payload, headers=headers)
    assert response.status_code == 200


@pytest.mark.parametrize(
    "model_parameters",
    [
        '{"temperature": 0.5, "maxTokens": 3000}',
        '{"temperature": 0.7, "maxTokens": 1500}',
        '{"temperature": 1.0, "maxTokens": 1000}',
    ],
)
def test_server_response_header_content_type(
    url_prompt_namespace, headers, payload, model_parameters
):
    """Test server response header content type."""
    headers["model-parameters"] = model_parameters
    response = requests.post(url_prompt_namespace, json=payload, headers=headers)
    assert response.headers["Content-Type"] == "application/json"


@pytest.mark.parametrize(
    "model_parameters",
    [
        '{"temperature": 0.5, "maxTokens": 3000}',
        '{"temperature": 0.7, "maxTokens": 1500}',
        '{"temperature": 1.0, "maxTokens": 1000}',
    ],
)
def test_server_response_content(
    url_prompt_namespace, headers, payload, model_parameters
):
    """Test server response content."""
    headers["model-parameters"] = model_parameters
    response = requests.post(url_prompt_namespace, json=payload, headers=headers)
    json_response = response.json()
    assert "generated" in json_response
    assert isinstance(json_response["generated"], str)
