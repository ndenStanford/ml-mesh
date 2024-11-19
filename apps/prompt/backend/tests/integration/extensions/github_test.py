"""Github test."""

# 3rd party libraries
import pytest
from github import GithubException

# Source
from src.extensions.github import github


@pytest.mark.order(0)
def test_github_write():
    """Github write method."""
    # ensure the file doesn't exist before attempting to write
    if github.exists("integration-tests/file"):
        github.rm("integration-tests/file", "Deleting existing test file")
    # assert that attempting to read a non-existent file raises an exception
    with pytest.raises(GithubException):
        github.read("integration-tests/file")
    # perform the write operation
    github.write("integration-tests/file", "integration tests", "")
    assert github.read("integration-tests/file") == ""


@pytest.mark.order(1)
def test_github_read():
    """Github write method."""
    assert github.read("integration-tests/file") == ""


@pytest.mark.order(2)
def test_github_ls():
    """Github write method."""
    assert github.ls("integration-tests") == ["integration-tests/file"]


@pytest.mark.order(3)
def test_github_delete():
    """Github write method."""
    github.rm("integration-tests/file", "")

    with pytest.raises(GithubException):
        github.read("integration-tests/file")
