"""Prompt tables test."""

# Standard Library
import os
from unittest.mock import patch

# 3rd party libraries
import pytest
from dyntastic import A, Dyntastic
from langchain_core.prompts.chat import BaseChatPromptTemplate

# Source
from src.extensions.github import GithubClient
from src.prompt.tables import PromptTemplate


@pytest.mark.parametrize(
    "alias, template, project",
    [
        ("prompt-1", "input: {text}", "project-1"),
    ],
)
def test_path(alias, template, project):
    """Test path method."""
    prompt = PromptTemplate(alias=alias, project=project, template=template)

    assert prompt.path == os.path.join(project, alias)


@pytest.mark.parametrize(
    "alias, template, project",
    [
        ("prompt-1", "input: {text}", "project-1"),
    ],
)
@patch.object(GithubClient, "write")
@patch.object(Dyntastic, "save")
def test_save(mock_dyntastic_save, mock_github_write, alias, template, project):
    """Test save."""
    # call
    prompt = PromptTemplate(alias=alias, project=project, template=template)
    prompt.save()
    # asserts
    mock_github_write.assert_called_with(
        os.path.join(project, alias),
        f"Add new prompt {alias}",
        prompt.template,
    )
    mock_dyntastic_save.assert_called_once()


@pytest.mark.parametrize(
    "alias, template, project",
    [
        ("prompt-1", "input: {text}", "project-1"),
    ],
)
@patch.object(GithubClient, "rm")
@patch.object(Dyntastic, "delete")
def test_delete(mock_dyntastic_delete, mock_github_rm, alias, template, project):
    """Test save."""
    # call
    prompt = PromptTemplate(alias=alias, project=project, template=template)
    prompt.delete()
    # asserts
    mock_github_rm.assert_called_with(
        os.path.join(project, alias), f"Delete prompt {alias}"
    )
    mock_dyntastic_delete.assert_called_once()


@pytest.mark.parametrize(
    "alias, template, project",
    [
        ("prompt-1", "input: {text}", "project-1"),
    ],
)
def test_as_langchain(alias, template, project):
    """Test langchain compatible mixin."""
    prompt = PromptTemplate(alias=alias, project=project, template=template)
    assert isinstance(prompt.as_langchain(), BaseChatPromptTemplate)


@pytest.mark.parametrize(
    "alias, template, project",
    [
        ("prompt-1", "input: {text}", "project-1"),
    ],
)
@patch.object(GithubClient, "read")
@patch.object(Dyntastic, "get")
def test_get(mock_dyntastic_get, mock_github_read, alias, template, project):
    """Test get."""
    mock_dyntastic_get.return_value = PromptTemplate(
        alias=alias, project=project, template=""
    )
    mock_github_read.return_value = template

    result = PromptTemplate.get(alias)

    mock_github_read.assert_called_with(os.path.join(project, alias))
    assert (
        result
        == PromptTemplate(alias=alias, project=project, template=template).model_dump()
    )


@patch.object(Dyntastic, "scan")
def test_scan(mock_dyntastic_scan):
    """Test scan all."""
    _ = PromptTemplate.scan()
    mock_dyntastic_scan.assert_called_once()


@pytest.mark.parametrize(
    "project",
    [
        ("project-1"),
    ],
)
@patch.object(Dyntastic, "scan")
def test_scanproject(mock_dyntastic_scan, project):
    """Test scan all."""
    _ = PromptTemplate.scan(project)
    mock_dyntastic_scan.assert_called_with(
        (A.project.is_in([project])), consistent_read=True
    )
