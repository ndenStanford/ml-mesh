"""Test routes.x"""

# Standard Library
from unittest.mock import patch

# 3rd party libraries
import pytest
from fastapi import status

# Source
from src.model.schemas import ModelSchema
from src.model.tables import ModelTable


def test_health_route(test_client):
    """Test health endpoint."""
    response = test_client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == "OK"


@patch.object(ModelSchema, "get")
def test_get_models(mock_model_get, test_client):
    """Test get models endpoint."""
    mock_model_get.return_value = []
    response = test_client.get("/api/v1/models", headers={"x-api-key": "1234"})
    mock_model_get.assert_called_once()
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"models": []}


def test_get_models_unauthenticated(test_client):
    """Test get models endpoint unauthenticated."""
    response = test_client.get("/api/v1/models")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "Not authenticated"}


@pytest.mark.parametrize("id", [1, 124543, "2423"])
@patch.object(ModelSchema, "get")
def test_get_model(mock_model_get, id, test_client):
    """Test get model endpoint."""
    mock_model_get.return_value = ModelSchema(id=id, model_name="test-model")
    response = test_client.get(f"/api/v1/models/{id}", headers={"x-api-key": "1234"})
    mock_model_get.assert_called_with(f"{id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "created_at": None,
        "id": f"{id}",
        "model_name": "test-model",
    }


def test_get_model_unauthenticated(test_client):
    """Test get model endpoint unauthenticated."""
    response = test_client.get("/api/v1/models/1")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "Not authenticated"}


# @pytest.mark.parametrize(
#     "id, model_name",
#     [
#         (124, "text-davinci-003"),
#         (
#             "1512",
#             "text-curie-001",
#         ),
#     ],
# )
# @patch("src.db.Model.save")
# def test_create_model(mock_table_save, id, model_name, test_client):
#     """Test get prompt endpoint."""
#     response = test_client.post(
#         f"/api/v1/models?model_name={model_name}", headers={"x-api-key": "1234"}
#     )

#     mock_table_save.assert_called_once()

#     assert response.status_code == status.HTTP_201_CREATED
#     data = response.json()

#     assert isinstance(data["id"], str)
#     assert isinstance(data["created_at"], str)
#     assert isinstance(data["model_name"], str)


# def test_create_model_unauthenticated(test_client):
#     """Test create model endpoint unauthenticated."""
#     response = test_client.post("/api/v1/models?model_name=model_name")
#     assert response.status_code == status.HTTP_403_FORBIDDEN
#     assert response.json() == {"detail": "Not authenticated"}


# @pytest.mark.parametrize(
#     "id, model_name, update",
#     [
#         (
#             124,
#             "text-davinci-004",
#             "text-davinci-005",
#         ),
#         (
#             "1512",
#             "text-curie-002",
#             "text-curie-003",
#         ),
#     ],
# )
# @patch.object(ModelSchema, "get")
# @patch("src.model.schemas.ModelSchema.update")
# def test_update_model(
#     mock_model_update, mock_model_get, id, model_name, update, test_client
# ):
#     """Test update model endpoint."""
#     mock_model_get.return_value = ModelSchema(id=id, model_name=model_name)
#     response = test_client.put(
#         f"/api/v1/models/{id}?model_name={update}", headers={"x-api-key": "1234"}
#     )
#     assert mock_model_get.call_count == 2
#     assert mock_model_update.call_count == 1
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json() == {
#         "created_at": None,
#         "id": f"{id}",
#         "model_name": model_name,
#     }


# def test_update_model_unauthenticated(test_client):
#     """Test update model endpoint unauthenticated."""
#     response = test_client.put("/api/v1/models/12345?model_name=model_name")
#     assert response.status_code == status.HTTP_403_FORBIDDEN
#     assert response.json() == {"detail": "Not authenticated"}


# @pytest.mark.parametrize("id", [1, 124543, "2423"])
# @patch.object(ModelTable, "get")
# @patch("src.model.tables.ModelTable.delete")
# def test_delete_model(mock_model_delete, mock_model_get, id, test_client):
#     """Test delete model endpoint."""
#     mock_model_get.return_value = ModelTable(id=id, model_name="test-model")

#     response = test_client.delete(f"/api/v1/models/{id}", headers={"x-api-key": "1234"})

#     assert mock_model_get.call_count == 1
#     assert mock_model_get.call_count == 1

#     mock_model_get.assert_called_with(f"{id}")

#     assert response.status_code == status.HTTP_200_OK
#     assert response.json() == "deleted"


# def test_delete_model_unauthenticated(test_client):
#     """Test delete model endpoint unauthenticated."""
#     response = test_client.delete("/api/v1/models/12345")
#     assert response.status_code == status.HTTP_403_FORBIDDEN
#     assert response.json() == {"detail": "Not authenticated"}
