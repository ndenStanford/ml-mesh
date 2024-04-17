"""Table tests."""

# Standard Library
import os
from unittest.mock import patch

# 3rd party libraries
import pytest
from dyntastic import Dyntastic

# Source
from src.extensions.github import GithubClient
from src.project.exceptions import ProjectInvalidAlias
from src.project.tables import Project


@pytest.mark.parametrize(
    "alias",
    [
        "new-project1",
        "new-project2",
        "new-project3",
    ],
)
def test_valid_alias(alias):
    """Test valid aliases."""
    _ = Project(alias=alias)


@pytest.mark.parametrize(
    "alias",
    [
        "new-project1*&",
    ],
)
def test_invalid_alias(alias):
    """Test valid aliases."""
    with pytest.raises(ProjectInvalidAlias):
        _ = Project(alias=alias)


@pytest.mark.parametrize(
    "alias",
    [
        "new-project1",
        "new-project2",
        "new-project3",
    ],
)
@patch.object(GithubClient, "write")
@patch.object(Dyntastic, "save")
def test_save(mock_dyntastic_save, mock_github_write, alias):
    """Test save."""
    # call
    project = Project(alias=alias)
    project.save()
    # asserts
    mock_github_write.assert_called_with(
        os.path.join(alias, ".gitkeep"), f"Create project {alias}", ""
    )
    mock_dyntastic_save.assert_called_once()
