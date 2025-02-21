"""Test routes."""

# Standard Library
from json import JSONDecodeError
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

# 3rd party libraries
import pytest
from dyntastic.exceptions import DoesNotExist
from fastapi import status
from langchain_core.exceptions import OutputParserException

# Source
from src.project.tables import Project
from src.prompt.exceptions import StrOutputParserTypeError
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
        "/api/v3/prompts", headers={"x-api-key": "1234"}, json=prompt.model_dump()
    )
    # asserts
    assert response.status_code == status.HTTP_201_CREATED
    mock_prompt_save.assert_called_once()
    assert response.json() == prompt.model_dump()


@pytest.mark.parametrize(
    "alias, new_template, project",
    [("existing-prompt", "new-template-text", "existing-project")],
)
@patch.object(PromptTemplate, "get")
@patch.object(PromptTemplate, "update")
def test_update_prompt(
    mock_prompt_update,
    mock_prompt_get,
    alias,
    new_template,
    project,
    test_client,
):
    """Test update prompt."""
    prompt = PromptTemplate(alias=alias, project=project, template="old-template")
    mock_prompt_get.return_value = prompt

    response = test_client.put(
        f"/api/v3/prompts/{alias}",
        headers={"x-api-key": "1234"},
        json={"template": new_template},
    )

    assert response.status_code == status.HTTP_201_CREATED
    mock_prompt_get.assert_called_once_with(alias)
    mock_prompt_update.assert_called_once()
    assert response.json() == {
        "alias": alias,
        "project": project,
        "template": new_template,
        "sha": None,
    }


@pytest.mark.parametrize(
    "alias, new_template, project",
    [("nonexistent-prompt", "new-template-text", "existing-project")],
)
@patch.object(PromptTemplate, "get")
def test_update_prompt_not_found(
    mock_prompt_get,
    alias,
    new_template,
    project,
    test_client,
):
    """Test update prompt not found."""
    mock_prompt_get.side_effect = DoesNotExist

    response = test_client.put(
        f"/api/v3/prompts/{alias}",
        headers={"x-api-key": "1234"},
        json={"template": new_template},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    mock_prompt_get.assert_called_once_with(alias)
    assert response.json() == {"detail": f"Prompt {alias} not found in database"}


@pytest.mark.parametrize(
    "alias, new_template, project",
    [("existing-prompt", "new-template-text", "existing-project")],
)
@patch.object(PromptTemplate, "get")
@patch.object(PromptTemplate, "update")
def test_update_prompt_unprocessable_entity(
    mock_prompt_update,
    mock_prompt_get,
    alias,
    new_template,
    project,
    test_client,
):
    """Test update prompt unprocessable entity."""
    prompt = PromptTemplate(alias=alias, project=project, template="old-template")
    mock_prompt_get.return_value = prompt
    mock_prompt_update.side_effect = Exception("Update failed")

    response = test_client.put(
        f"/api/v3/prompts/{alias}",
        headers={"x-api-key": "1234"},
        json={"template": new_template},
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    mock_prompt_get.assert_called_once_with(alias)
    mock_prompt_update.assert_called_once()
    assert response.json() == {"detail": "Update failed"}


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
        f"/api/v3/prompts/{alias}",
        headers={"x-api-key": "1234"},
    )
    # asserts
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == prompt.model_dump()
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
        f"/api/v3/prompts/{alias}",
        headers={"x-api-key": "1234"},
    )
    # asserts
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == prompt.model_dump()
    mock_prompt_get.assert_called_with(alias)


@patch.object(PromptTemplate, "scan")
def test_list_prompt(mock_prompt_scan, test_client):
    """Test list prompt."""
    # call
    response = test_client.get("/api/v3/prompts", headers={"x-api-key": "1234"})
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
        f"/api/v3/prompts/{alias}/generate/model/{model}",
        headers={"x-api-key": "1234"},
        json=values,
    )
    mock_generate.assert_called_with(alias, model, **values, model_parameters=None)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
    "alias, model, values",
    [("prompt-1", "model-1", {"text": ""})],
)
@patch("src.prompt.functional.generate_from_prompt_template.apply_async")
@patch("src.prompt.functional.Generated")
@patch("src.prompt.functional.Generated.save")
def test_generate_async(
    mock_generated_save,
    mock_generated,
    mock_generate,
    alias,
    model,
    values,
    test_client,
):
    """Test get generate from prompt template endpoint."""
    mock_generated_instance = MagicMock()
    mock_generated.return_value = mock_generated_instance
    mock_generate.return_value = SimpleNamespace(**{"id": "1234"})
    response = test_client.post(
        f"/api/v3/prompts/{alias}/generate/async/model/{model}",
        headers={"x-api-key": "1234"},
        json=values,
    )
    mock_generate.assert_called_once()
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
    "alias, model, values, exception",
    [
        (
            "prompt-1",
            "model-1",
            {"text": ""},
            JSONDecodeError("JSON decode error", "source", 102),
        ),
        (
            "prompt-2",
            "model-2",
            {"text": ""},
            OutputParserException("Output parser exception"),
        ),
        (
            "prompt-3",
            "model-3",
            {"text": ""},
            StrOutputParserTypeError(),
        ),
    ],
)
@patch("src.prompt.functional.generate_from_prompt_template")
def test_generate_exception(
    mock_generate, alias, model, values, exception, test_client
):
    """Test get generate from prompt template endpoint with exceptions."""
    mock_generate.side_effect = [exception]

    response = test_client.post(
        f"/api/v3/prompts/{alias}/generate/model/{model}",
        headers={"x-api-key": "1234"},
        json=values,
    )
    if isinstance(exception, JSONDecodeError):
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert (
            response.json()["detail"]
            == "JSONDecodeError: JSON decode error: line 1 column 103 (char 102)"
        )
    elif isinstance(exception, OutputParserException):
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert (
            response.json()["detail"]
            == "OutputParserException: Output parser exception\nFor troubleshooting, visit: https://python.langchain.com/docs/troubleshooting/errors/OUTPUT_PARSING_FAILURE"
        )
    elif isinstance(exception, StrOutputParserTypeError):
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            response.json()["detail"]
            == "StrOutputParserTypeError: str_output_parser must be a boolean value"
        )
    mock_generate.assert_called_with(alias, model, **values, model_parameters=None)


@pytest.mark.parametrize(
    "alias, values",
    [("prompt-1", {"text": ""}), ("prompt-2", {"text": ""})],
)
@patch("src.prompt.functional.generate_from_default_model")
def test_generate_from_default_model(mock_generate, alias, values, test_client):
    """Test get model endpoint."""
    response = test_client.post(
        f"/api/v3/prompts/{alias}/generate",
        headers={"x-api-key": "1234"},
        json=values,
    )
    mock_generate.assert_called_with(alias, **values)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
    "alias, values",
    [("prompt-1", {"text": ""}), ("prompt-2", {"text": ""})],
)
@patch("src.prompt.functional.generate_from_default_model.apply_async")
@patch("src.prompt.functional.Generated")
@patch("src.prompt.functional.Generated.save")
def test_generate_from_default_model_async(
    mock_generated_save, mock_generated, mock_generate, alias, values, test_client
):
    """Test get model endpoint."""
    mock_generated_instance = MagicMock()
    mock_generated.return_value = mock_generated_instance
    mock_generate.return_value = SimpleNamespace(**{"id": "1234"})
    response = test_client.post(
        f"/api/v3/prompts/{alias}/generate/async",
        headers={"x-api-key": "1234"},
        json=values,
    )
    mock_generate.assert_called_once()
    assert response.status_code == status.HTTP_200_OK
