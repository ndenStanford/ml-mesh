"""Model namespace tests."""

# 3rd party libraries
import pytest
import requests


@pytest.mark.parametrize(
    "data",
    [
        {
            "id": "qwer6ty7",
            "status": "str",
            "generation": {"generated": "generated-1"},
            "prompt": "english-summarization",
            "model": "gpt-4o",
            "model_parameters": {"temperature": "0.5"},
            "timestamp": "2024-11-19T12:00:00",
        }
    ],
)
def test_server_response_status_code(url_generated_namespace, headers, data):
    """Test server response code."""
    response = requests.post(url_generated_namespace, headers=headers, json=data)
    assert response.status_code == 201


@pytest.mark.parametrize(
    "data",
    [
        {
            "id": "qwer6y6",
            "status": "str",
            "generation": {"generated": "generated-1"},
            "prompt": "english-summarization",
            "model": "gpt-4o",
            "model_parameters": {"temperature": "0.5"},
            "timestamp": "2024-11-19T12:00:00",
        }
    ],
)
def test_response_header_content_type(url_generated_namespace, headers, data):
    """Test response header content type."""
    response = requests.post(url_generated_namespace, headers=headers, json=data)
    assert response.headers["Content-Type"] == "application/json"
