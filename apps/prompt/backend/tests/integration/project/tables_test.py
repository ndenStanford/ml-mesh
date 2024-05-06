"""Project routes test."""

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
def test_save(alias, app):
    """Test save."""
    project = Project(alias=alias)
    project.save()
    assert alias in github.ls("")


@pytest.mark.parametrize(
    "alias",
    ["integration-test"],
)
@pytest.mark.order(9)
def test_delete(alias, app):
    """Test delete."""
    project = Project(alias=alias)
    project.delete()
    assert Project.safe_get(alias) is None
