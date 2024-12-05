"""Routes tests."""

# Standard Library
from unittest.mock import patch

# 3rd party libraries
import pytest
from fastapi import status

# Source
from src.project.tables import Project
from src.prompt.tables import PromptTemplate


@pytest.mark.parametrize(
    "alias",
    [
        "new-project1",
        "new-project2",
        "new-project3",
    ],
)
@patch.object(Project, "save")
@patch.object(Project, "safe_get")
def test_create_project(mock_project_safe_get, mock_project_save, alias, test_client):
    """Test create project endpoint."""
    # setup
    mock_project_safe_get.return_value = None
    # mock call
    response = test_client.post(
        f"/api/v3/projects?alias={alias}", headers={"x-api-key": "1234"}
    )
    # asserts
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"alias": alias}
    mock_project_save.assert_called_once()
    mock_project_safe_get.assert_called_with(alias)


@pytest.mark.parametrize(
    "alias",
    [
        "new-project1",
        "new-project2",
        "new-project3",
    ],
)
@patch.object(Project, "delete")
@patch.object(Project, "get")
def test_delete_project(mock_project_get, mock_project_delete, alias, test_client):
    """Test project delete endpoint."""
    # setup
    mock_project_get.return_value = Project(alias=alias)
    # call
    response = test_client.delete(
        f"/api/v3/projects/{alias}", headers={"x-api-key": "1234"}
    )
    # asserts
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"alias": alias}
    mock_project_delete.assert_called_once()
    mock_project_get.assert_called_with(alias)


@patch.object(Project, "scan")
def test_list_projects(mock_project_scan, test_client):
    """List projects endpoint."""
    # call
    response = test_client.get("/api/v3/projects", headers={"x-api-key": "1234"})
    # asserts
    assert response.status_code == status.HTTP_200_OK
    mock_project_scan.assert_called_once()


@pytest.mark.parametrize(
    "alias",
    [
        "new-project1",
        "new-project2",
        "new-project3",
    ],
)
@patch.object(Project, "get")
def test_get_project(mock_project_get, alias, test_client):
    """Test get project endpoint."""
    # setup
    mock_project_get.return_value = Project(alias=alias)
    # call
    response = test_client.get(
        f"/api/v3/projects/{alias}", headers={"x-api-key": "1234"}
    )
    # asserts
    assert response.status_code == status.HTTP_200_OK
    response.json() == {"alias": alias}


@patch.object(PromptTemplate, "scan")
def test_list_prompts(mock_project_scan, test_client):
    """Test list project endpoint."""
    # call
    response = test_client.get(
        "/api/v3/projects/new-project/prompts", headers={"x-api-key": "1234"}
    )
    # asserts
    assert response.status_code == status.HTTP_200_OK
    mock_project_scan.assert_called_once()
