"""Routes test."""

# 3rd party libraries
import pytest
from fastapi import status


def test_get_models(test_client, create_models):
    """Test get models endpoint."""
    response = test_client.get("/api/v1/models", headers={"x-api-key": "1234"})

    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(data["models"]) == 4


def test_get_model(test_client, create_models):
    """Test get model endpoint."""
    model = create_models[1]

    response = test_client.get(
        f"/api/v1/models/{model.id}", headers={"x-api-key": "1234"}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == model.id
    assert response.json()["model_name"] == model.model_name
    assert response.json()["created_at"] == model.created_at
    assert response.json()["max_tokens"] == model.max_tokens
    assert response.json()["temperature"] == model.temperature


@pytest.mark.parametrize(
    "id",
    [
        "abc",
        "efg",
    ],
)
def test_get_model_fail(test_client, create_models, id):
    """Test get model endpoint."""
    response = test_client.get(f"/api/v1/models/{id}", headers={"x-api-key": "1234"})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Item does not exist - (id={})".format(id)}
