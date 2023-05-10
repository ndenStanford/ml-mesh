"""Test routes."""


# 3rd party libraries
from fastapi import status


def test_health_route(test_client):
    """Test health endpoint."""
    response = test_client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == "OK"


def test_entity_link_prompt(
    example_content_input, example_entities_input, example_entities_output, test_client
):
    """Test entity linking endpoint."""
    response = test_client.post(
        "/entity-linking/fish",
        json={"content": example_content_input, "entities": example_entities_input},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"entities": example_entities_output}
