"""Tables test."""

# Standard Library
import os

# 3rd party libraries
import pytest
from dyntastic.exceptions import DoesNotExist

# Source
from src.extensions.github import github
from src.prompt.tables import PromptTemplate


@pytest.mark.parametrize(
    "alias, template, project",
    [
        ("prompt-12", "input: {text}", "integration-test-1"),
    ],
)
@pytest.mark.order(14)
def test_save(alias, template, project, app):
    """Test save method."""
    with pytest.raises(DoesNotExist):
        _ = PromptTemplate.get(alias)

    prompt = PromptTemplate(alias=alias, template=template, project=project)
    prompt.save()

    assert PromptTemplate.get(alias).model_dump_json() == prompt.model_dump_json()
    assert os.path.join(project, alias) in github.ls(project)


@pytest.mark.parametrize(
    "alias, template, project",
    [
        ("prompt1", "Hello! How are you?", "integration-test-1"),
    ],
)
@pytest.mark.order(15)
def test_delete(alias, template, project, app):
    """Test delete method."""
    prompt = PromptTemplate(alias=alias, template=template, project=project)
    assert PromptTemplate.get(alias).model_dump_json(
        exclude={"sha"}
    ) == prompt.model_dump_json(exclude={"sha"})

    prompt.delete()

    with pytest.raises(DoesNotExist):
        _ = PromptTemplate.get(alias)


@pytest.mark.order(16)
def test_scan_all(create_prompts, app):
    """Test scan."""
    prompts = list(PromptTemplate.scan())
    assert len(prompts) >= 2


@pytest.mark.parametrize(
    "project, expected",
    [
        ("integration-test-2", 2),
    ],
)
@pytest.mark.order(17)
def test_scan_project(project, expected, app):
    """Test scan."""
    prompts = list(PromptTemplate.scan(project))
    assert len(prompts) == expected
