"""Model namespace tests."""

# 3rd party libraries
import pytest
import requests


@pytest.mark.parametrize(
    "data",
    [
        {
            "id": "e2978cc2-08ec-42bc-928a-c9e59c3fafe",
            "generation": "test1",
            "method": "src.prompt.functional.generate_from_prompt_template",
            "args": ["english-summarization", "gpt-4o"],
            "kwargs": {"input": {"number": 5, "text": "What is the capital of US?"}},
            "timestamp": "2024-11-19T12:00:00",
        }
    ],
)
def test_server_response_status_code(url_generated_namespace, headers, data):
    """Test server response code."""
    response = requests.post(url_generated_namespace, headers=headers, json=data)
    print(response.text)
    assert response.status_code == 201


@pytest.mark.parametrize(
    "data",
    [
        {
            "id": "e2977cc2-08ec-42bc-928a-c9e59c3fafe",
            "generation": "test1",
            "method": "src.prompt.functional.generate_from_prompt_template",
            "args": ["english-summarization", "gpt-4o"],
            "kwargs": {"input": {"number": 5, "text": "What is the capital of US?"}},
            "timestamp": "2024-11-19T12:00:00",
        }
    ],
)
def test_response_header_content_type(url_generated_namespace, headers, data):
    """Test response header content type."""
    response = requests.post(url_generated_namespace, headers=headers, json=data)
    assert response.headers["Content-Type"] == "application/json"
