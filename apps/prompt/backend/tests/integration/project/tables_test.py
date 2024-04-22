"""Project routes test."""

# Standard Library
import os

# 3rd party libraries
import pytest

# Source
from src.extensions.github import github
from src.project.tables import Project


@pytest.mark.parametrize(
    "alias",
    ["integration-test"],
)
@pytest.mark.order(8)
def test_save(alias):
    """Test save."""
    project = Project(alias=alias)
    project.save()
    assert os.path.join(alias, ".gitkeep") in github.ls("")


@pytest.mark.parametrize(
    "alias",
    ["integration-test"],
)
@pytest.mark.order(9)
def test_delete(alias):
    """Test delete."""
    project = Project(alias=alias)
    project.delete()
    assert Project.safe_get(alias) is None
