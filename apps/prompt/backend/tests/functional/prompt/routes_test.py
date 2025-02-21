"""Prompt namespace tests."""

# Standard Library
import time

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


@pytest.mark.parametrize(
    "model_parameters",
    [
        '{"temperature": 0.5, "maxTokens": 3000}',
        '{"temperature": 0.7, "maxTokens": 1500}',
        '{"temperature": 1.0, "maxTokens": 1000}',
    ],
)
def test_server_response_content_async(
    url_generated_namespace,
    url_prompt_namespace_async,
    headers,
    payload,
    model_parameters,
):
    """Test server response content with Celery integration."""
    headers["model-parameters"] = model_parameters

    response = requests.post(url_prompt_namespace_async, json=payload, headers=headers)
    json_response = response.json()

    assert "id" in json_response
    task_id = json_response["id"]

    status_url = f"{url_generated_namespace}{task_id}"
    max_wait_time = 10
    start_time = time.time()

    while True:
        status_response = requests.get(status_url, headers=headers)
        status_json = status_response.json()

        if status_json["status"] == "SUCCESS":
            assert "generated" in status_json["generation"]
            assert isinstance(status_json["generation"]["generated"], str)
            break

        elif status_json["status"] == "FAILURE":
            pytest.fail(f"Task failed with error: {status_json.get('error')}")

        if time.time() - start_time > max_wait_time:
            pytest.fail("Task did not complete within 10 seconds")

        time.sleep(1)
