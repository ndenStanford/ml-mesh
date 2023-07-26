"""Test routes."""


# 3rd party libraries
from fastapi import status


def test_health_route(test_client):
    """Test health endpoint."""
    response = test_client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == "OK"


def test_lsh_prompt(example_content_input, example_lsh_output, test_client):
    """Test lsh linking endpoint."""
    response = test_client.post(
        "/lsh",
        json={"content": example_content_input, "signature": example_lsh_input},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"signature": example_lsh_output}


def test_empty_input(test_client):
    """Test lsh endpoint with empty input."""
    response = test_client.post(
        "/lsh",
        json={"content": "", "signature": None},  # Empty content input
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "content"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }
