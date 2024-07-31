"""Local filesystem test."""

# Standard Library
from unittest.mock import patch

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.io import LocalFileSystem, OnclusivePath


@pytest.mark.parametrize(
    "path",
    [OnclusivePath("file:///folder/file.txt"), OnclusivePath("file:///")],
)
@patch("builtins.open")
def test_open(mock_open, path):
    """Test open method."""
    local_fs = LocalFileSystem()

    _ = local_fs.open(path)
    mock_open.assert_called_with(
        path.name, mode="r", encoding=None, errors=None, newline=None
    )


@pytest.mark.parametrize(
    "source, destination",
    [
        (
            OnclusivePath("file:///source/file.txt"),
            OnclusivePath("file:///destination/file.txt"),
        ),
    ],
)
@patch("shutil.copyfile")
def test_cp(source, destination):
    local_fs = LocalFileSystem()

    f = local_fs.open(path)


def test_exists():
    ...


def test_glob():
    ...


def test_isdir():
    ...


def test_ls():
    ...


def test_mkdirs():
    ...


def test_mkdir():
    ...
