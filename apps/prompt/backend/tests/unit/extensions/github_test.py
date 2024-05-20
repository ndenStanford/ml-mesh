"""Github test."""

# Standard Library
from dataclasses import dataclass
from unittest.mock import patch

# 3rd party libraries
import pytest
from github import GithubIntegration

# Source
from src.extensions.github import github
from src.settings import get_settings


settings = get_settings()


@dataclass
class MockContentFile:
    """Mock ContentFile object."""

    name: str
    type: str
    path: str
    sha: str = ""


@patch.object(GithubIntegration, "__new__")
@patch("github.Auth.AppAuth")
def test_initialize_client(github_auth_mock, github_integration_mock):
    """Test client."""
    _ = github.repo

    github_auth_mock.assert_called_once()
    github_integration_mock.assert_called_once()


@pytest.mark.parametrize(
    "path, commit, contents",
    [("repo/folder/file.extension", "commit message", "contents")],
)
@patch.object(GithubIntegration, "__new__")
@patch("github.Auth.AppAuth")
def test_write(github_auth_mock, github_integration_mock, path, commit, contents):
    """Test write."""
    _ = github.write(path, commit, contents)
    get_installations = (
        github_integration_mock.return_value.get_installations.return_value
    )
    get_installations.__getitem__.return_value.get_github_for_installation.return_value.get_repo.return_value.create_file.assert_called_with(  # noqa: E501
        path, commit, contents
    )


@pytest.mark.parametrize(
    "path, contents",
    [("repo/folder/file.extension", b'{"key":"value"}'), ("", b"{}")],
)
@patch.object(GithubIntegration, "__new__")
@patch("github.Auth.AppAuth")
def test_read(github_auth_mock, github_integration_mock, path, contents):
    """Test read."""
    _ = github.read(path)
    get_installations = (
        github_integration_mock.return_value.get_installations.return_value
    )
    get_github_for_installation = (
        get_installations.__getitem__.return_value.get_github_for_installation.return_value
    )
    get_contents = (
        get_github_for_installation.get_repo.return_value.get_contents.return_value
    )
    get_contents.type = "file"
    get_contents.decoded_content.decode.return_value = contents
    read_result = github.read(path)
    get_github_for_installation.get_repo.return_value.get_contents.assert_called_with(  # noqa: E501
        path
    )
    assert read_result == contents


@pytest.mark.parametrize(
    "path, contentfiles, expected",
    [
        (
            "folder",
            [
                MockContentFile(name="filename", path="folder/filename", type="file"),
                MockContentFile(name=".gitkeep", path="folder/.gitkeep", type="file"),
            ],
            ["folder/filename"],
        )
    ],
)
@patch.object(GithubIntegration, "__new__")
@patch("github.Auth.AppAuth")
def test_ls(github_auth_mock, github_integration_mock, path, contentfiles, expected):
    """Test ls method."""
    get_installations = (
        github_integration_mock.return_value.get_installations.return_value
    )
    get_github_for_installation = (
        get_installations.__getitem__.return_value.get_github_for_installation.return_value
    )
    get_contents = get_github_for_installation.get_repo.return_value.get_contents
    get_contents.return_value = contentfiles

    files = github.ls(path)

    get_contents.assert_called_with(path)

    assert files == expected


@pytest.mark.parametrize(
    "path, contentfiles",
    [
        (
            "folder",
            [
                MockContentFile(name="filename1", path="folder/filename1", type="file"),
                MockContentFile(name="filename2", path="folder/filename2", type="file"),
            ],
        ),
        (
            "folder",
            MockContentFile(name="filename", path="folder/filename", type="file"),
        ),
    ],
)
@patch.object(GithubIntegration, "__new__")
@patch("github.Auth.AppAuth")
def test_rm(github_auth_mock, github_integration_mock, path, contentfiles):
    """Test rm method."""
    get_installations = (
        github_integration_mock.return_value.get_installations.return_value
    )
    get_github_for_installation = (
        get_installations.__getitem__.return_value.get_github_for_installation.return_value
    )
    get_contents = get_github_for_installation.get_repo.return_value.get_contents
    get_contents.return_value = contentfiles

    _ = github.rm(path, "")

    get_contents.assert_called_with(path)

    if not isinstance(contentfiles, list):
        get_github_for_installation.get_repo.return_value.delete_file.assert_called_once()
    else:
        assert (
            get_github_for_installation.get_repo.return_value.delete_file.call_count
            == len(contentfiles)
        )
