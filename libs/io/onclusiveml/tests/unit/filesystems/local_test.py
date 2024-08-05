"""Local filesystem test."""

# Standard Library
import datetime
import os
from unittest.mock import patch

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.io import OnclusivePath


@pytest.mark.parametrize(
    "path",
    [OnclusivePath("file:///folder/file.txt"), OnclusivePath("file:///")],
)
@patch("builtins.open")
def test_open(mock_open, localfs, path):
    """Test open method."""
    _ = localfs.open(path)
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
def test_cp(mock_copyfile, localfs, source, destination):
    """Test copy."""
    localfs.cp(source, destination)
    mock_copyfile.assert_called_with(source.name, destination.name)


@pytest.mark.parametrize(
    "path",
    [
        OnclusivePath("file:///folder/file.txt"),
        OnclusivePath("file:///bin/local/script.py"),
    ],
)
@patch("os.path.exists")
def test_exists_file(mock_exists, localfs, path):
    """Tests exists method for file."""
    mock_exists.return_value = True

    assert localfs.exists(path)

    mock_exists.assert_called_with(path._raw_path)


@pytest.mark.parametrize(
    "path",
    [OnclusivePath("file:///folder"), OnclusivePath("file:///bin/local/")],
)
@patch("os.path.exists")
def test_exists_dir(mock_exists, localfs, path):
    """Tests exists method for folder."""
    mock_exists.return_value = True

    assert localfs.exists(path)

    mock_exists.assert_called_with(path._raw_path)


@pytest.mark.parametrize(
    "path, glob",
    [
        (
            OnclusivePath("file:///folder/subfolder/*"),
            [
                OnclusivePath("file:///folder/subfolder/filea"),
                OnclusivePath("file:///folder/subfolder/fileb"),
            ],
        )
    ],
)
@patch("os.path.exists")
@patch("glob.glob")
def test_exists_glob(mock_glob, mock_exists, localfs, path, glob):
    """Tests exists method for folder."""
    mock_exists.return_value = True
    mock_glob.return_value = glob

    assert localfs.exists(path)

    mock_glob.assert_called_with(path._raw_path)


@pytest.mark.parametrize(
    "path, glob",
    [
        (
            OnclusivePath("file:///folder/subfolder/*"),
            [
                OnclusivePath("file:///folder/subfolder/filea"),
                OnclusivePath("file:///folder/subfolder/fileb"),
            ],
        )
    ],
)
@patch("glob.glob")
def test_glob(mock_glob, localfs, path, glob):
    """Test glob method."""
    mock_glob.return_value = glob

    assert localfs.glob(path)

    mock_glob.assert_called_with(path._raw_path)


@pytest.mark.parametrize(
    "path, expected",
    [
        (OnclusivePath("file:///folder/subfolder/*"), False),
        (OnclusivePath("file:///folder/subfolder/file.extension"), False),
        (OnclusivePath("file:///folder/subfolder/"), True),
    ],
)
@patch("os.path.isdir")
def test_isdir(mock_isdir, localfs, path, expected):
    """Test isdir method."""
    mock_isdir.return_value = expected

    assert localfs.isdir(path) == expected
    mock_isdir.assert_called_with(path._raw_path)


@pytest.mark.parametrize(
    "path, expected",
    [
        (OnclusivePath("file:///folder/subfolder/*"), False),
        (OnclusivePath("file:///folder/subfolder/file.extension"), True),
        (OnclusivePath("file:///folder/subfolder/"), False),
    ],
)
@patch("os.path.isfile")
def test_isfile(mock_isfile, localfs, path, expected):
    """Test isfile method."""
    mock_isfile.return_value = expected

    assert localfs.isfile(path) == expected
    mock_isfile.assert_called_with(path._raw_path)


@pytest.mark.parametrize(
    "path, isdir_return",
    [
        (OnclusivePath("file:///folder/subfolder/"), True),
    ],
)
@patch("os.path.isdir")
@patch("os.makedirs")
def test_mkdirs(mock_mkdirs, mock_isdir, localfs, path, isdir_return):
    """Test mkdirs method."""
    mock_isdir.return_value = isdir_return
    mock_mkdirs.return_value = None

    assert localfs.mkdirs(path) is None
    mock_isdir.assert_called_with(path._raw_path)
    mock_mkdirs.assert_called_with(path._raw_path, exist_ok=True)


@pytest.mark.parametrize(
    "path, isdir",
    [
        (OnclusivePath("file:///folder/subfolder/"), True),
    ],
)
@patch("os.path.isdir")
@patch("os.mkdir")
def test_mkdir(mock_mkdir, mock_isdir, localfs, path, isdir):
    """Test mkdir method."""
    mock_isdir.return_value = isdir

    assert localfs.mkdir(path) is None
    mock_mkdir.assert_called_with(path._raw_path)


@pytest.mark.parametrize(
    "path, isfile",
    [
        (OnclusivePath("file:///folder/subfolder/file.pt"), True),
    ],
)
@patch("os.path.isfile")
@patch("os.remove")
def test_rm_file(mock_remove, mock_isfile, localfs, path, isfile):
    """Test rm method."""
    mock_isfile.return_value = isfile
    mock_remove.return_value = None

    assert localfs.rm(path) is None
    mock_remove.assert_called_with(path._raw_path)


@pytest.mark.parametrize(
    "path, isfile, os_stat, expected",
    [
        (
            OnclusivePath("file:///home/ec2-dev/ml-mesh/poetry.lock"),
            True,
            os.stat_result(
                (
                    33204,
                    12,
                    66307,
                    1,
                    0,
                    100,
                    584501,
                    1712652148,
                    1712652148,
                    1722603730,
                )
            ),
            {
                "size": 584501,
                "created": datetime.datetime.fromtimestamp(1722603730),
                "last_modified": datetime.datetime.fromtimestamp(1712652148),
                "path": "/home/ec2-dev/ml-mesh/poetry.lock",
            },
        )
    ],
)
@patch("os.path.isfile")
@patch("os.stat")
def test_info(mock_os_stat, mock_isfile, localfs, path, isfile, os_stat, expected):
    """Test file info."""
    mock_os_stat.return_value = os_stat
    mock_isfile.return_value = isfile

    info = localfs.info(path)

    assert info.size == expected["size"]
    assert info.created == expected["created"]
    assert info.last_modified == expected["last_modified"]
    assert info.path == expected["path"]
