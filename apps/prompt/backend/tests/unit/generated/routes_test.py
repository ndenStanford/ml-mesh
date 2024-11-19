"""Routes tests."""

# Standard Library
from unittest.mock import patch

# 3rd party libraries
import pytest
from fastapi import status

# Source
from src.generated.tables import Generated


@pytest.mark.parametrize(
    "id",
    [
        "e2978cc1-08ec-42bc-928a-c9e59c3fafe",
        "e2678cc1-08ec-42bc-928a-c9e59k5oapt",
    ],
)
@patch.object(Generated, "save")
@patch.object(Generated, "safe_get")
def test_create_project(mock_generated_safe_get, mock_generated_save, id, test_client):
    """Test save generated endpoint."""
    # setup
    mock_generated_safe_get.return_value = None
    # mock call
    response = test_client.post(
        f"/api/v3/generated?id={id}", headers={"x-api-key": "1234"}
    )
    # asserts
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"id": id}
    mock_generated_save.assert_called_once()
    mock_generated_safe_get.assert_called_with(id)


@pytest.mark.parametrize(
    "id",
    [
        "e2978cc1-08ec-42bc-928a-c9e59c3fafe",
        "e2678cc1-08ec-42bc-928a-c9e59k5oapt",
    ],
)
@patch.object(Generated, "delete")
@patch.object(Generated, "get")
def test_delete_project(mock_generated_get, mock_generated_delete, id, test_client):
    """Test generated delete endpoint."""
    # setup
    mock_generated_get.return_value = Generated(id=id)
    # call
    response = test_client.delete(
        f"/api/v3/generated/{id}", headers={"x-api-key": "1234"}
    )
    # asserts
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"id": id}
    mock_generated_delete.assert_called_once()
    mock_generated_get.assert_called_with(id)


@pytest.mark.parametrize(
    "id",
    [
        "e2978cc1-08ec-42bc-928a-c9e59c3fafe",
        "e2678cc1-08ec-42bc-928a-c9e59k5oapt",
    ],
)
@patch.object(Generated, "get")
def test_get_project(mock_generated_get, id, test_client):
    """Test get generated endpoint."""
    # setup
    mock_generated_get.return_value = Generated(id=id)
    # call
    response = test_client.get(f"/api/v3/generated/{id}", headers={"x-api-key": "1234"})
    # asserts
    assert response.status_code == status.HTTP_200_OK
    response.json() == {"id": id}
