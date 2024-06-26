"""Test routes."""

# Standard Library
from unittest.mock import patch

# 3rd party libraries
import pytest
from fastapi import status

# Source
from src.project.tables import Project
from src.prompt.tables import PromptTemplate


@pytest.mark.parametrize(
    "alias, template, project",
    [("new-prompt", "{text}", "new-project1")],
)
@patch.object(Project, "get")
@patch.object(PromptTemplate, "get")
@patch.object(PromptTemplate, "save")
def test_create_prompt(
    mock_prompt_save,
    mock_prompt_get,
    mock_project_get,
    alias,
    template,
    project,
    test_client,
):
    """Test create prompt."""
    # setup
    prompt = PromptTemplate(alias=alias, project=project, template=template)
    mock_prompt_get.return_value = prompt
    mock_project_get.return_value = Project(alias=project)
    # api call
    response = test_client.post(
        "/api/v2/prompts", headers={"x-api-key": "1234"}, json=prompt.dict()
    )
    # asserts
    assert response.status_code == status.HTTP_201_CREATED
    mock_prompt_save.assert_called_once()
    assert response.json() == prompt.dict()


@pytest.mark.parametrize(
    "alias, template, project",
    [("new-prompt", "{text}", "new-project1")],
)
@patch.object(PromptTemplate, "delete")
@patch.object(PromptTemplate, "get")
def test_delete_prompt(
    mock_prompt_get, mock_prompt_delete, alias, template, project, test_client
):
    """Test delete prompt."""
    # setup
    prompt = PromptTemplate(alias=alias, project=project, template=template)
    mock_prompt_get.return_value = prompt
    # api call
    response = test_client.delete(
        f"/api/v2/prompts/{alias}",
        headers={"x-api-key": "1234"},
    )
    # asserts
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == prompt.dict()
    mock_prompt_delete.assert_called_once()
    mock_prompt_get.assert_called_with(alias)


@pytest.mark.parametrize(
    "alias, template, project",
    [("new-prompt", "{text}", "new-project1")],
)
@patch.object(PromptTemplate, "get")
def test_get_prompt(mock_prompt_get, alias, template, project, test_client):
    """Test get prompt."""
    prompt = PromptTemplate(alias=alias, project=project, template=template)
    mock_prompt_get.return_value = prompt
    # api call
    response = test_client.get(
        f"/api/v2/prompts/{alias}",
        headers={"x-api-key": "1234"},
    )
    # asserts
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == prompt.dict()
    mock_prompt_get.assert_called_with(alias)


@patch.object(PromptTemplate, "scan")
def test_list_prompt(mock_prompt_scan, test_client):
    """Test list prompt."""
    # call
    response = test_client.get("/api/v2/prompts", headers={"x-api-key": "1234"})
    # asserts
    assert response.status_code == status.HTTP_200_OK
    mock_prompt_scan.assert_called_once()


@pytest.mark.parametrize(
    "alias, model, values",
    [("prompt-1", "model-1", {"text": ""})],
)
@patch("src.prompt.functional.generate_from_prompt_template")
def test_generate(mock_generate, alias, model, values, test_client):
    """Test get generate from prompt template endpoint."""
    response = test_client.post(
        f"/api/v2/prompts/{alias}/generate/model/{model}",
        headers={"x-api-key": "1234"},
        json=values,
    )
    mock_generate.assert_called_with(alias, model, **values, model_parameters=None)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
    "alias, values",
    [("prompt-1", {"text": ""}), ("prompt-2", {"text": ""})],
)
@patch("src.prompt.functional.generate_from_default_model")
def test_generate_from_default_model(mock_generate, alias, values, test_client):
    """Test get model endpoint."""
    response = test_client.post(
        f"/api/v2/prompts/{alias}/generate",
        headers={"x-api-key": "1234"},
        json=values,
    )
    mock_generate.assert_called_with(alias, **values)
    assert response.status_code == status.HTTP_200_OK
