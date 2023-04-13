"""Routes test."""

# 3rd party libraries
import pytest
from fastapi import status

# Source
from src.model.schemas import ModelSchema
from src.model.tables import ModelTable


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


@pytest.mark.parametrize(
    "model_name",
    [
        "text-davinci-009",
    ],
)
def test_create_model(model_name, test_client):
    """Test get model endpoint."""
    response = test_client.post(
        f"/api/v1/models?model_name={model_name}", headers={"x-api-key": "1234"}
    )

    data = response.json()
    model = ModelSchema.get(id=data["id"])

    assert response.status_code == status.HTTP_201_CREATED
    assert isinstance(data["id"], str)
    assert isinstance(data["created_at"], str)
    assert isinstance(data["model_name"], str)
    assert model.id == data["id"]
    assert model.created_at == data["created_at"]
    assert model.model_name == data["model_name"]


def test_update_model(test_client, create_models):
    """Test update model endpoint."""

    model = create_models[2]

    response = test_client.put(
        f"/api/v1/models/{model.id}?model_name=updated model_name",
        headers={"x-api-key": "1234"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "created_at": model.created_at,
        "id": model.id,
        "model_name": "updated model_name",
    }


def test_delete_model(test_client, create_models):
    """Test delete model endpoint."""

    model = create_models[3]

    response = test_client.delete(
        f"/api/v1/models/{model.id}", headers={"x-api-key": "1234"}
    )

    with pytest.raises(ModelTable.DoesNotExist):
        _ = ModelSchema.get(id=model.id)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == "deleted"
