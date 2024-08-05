"""Local filesystem integration tests."""

# Standard Library
import datetime

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.io import OnclusivePath


@pytest.mark.parametrize(
    "path",
    [OnclusivePath.from_relative("tests/integration/data/test_files/file1.md")],
)
def test_open_bytes(localfs, path):
    """Test open."""
    with localfs.open(path, mode="rb") as f:
        assert isinstance(f.read(), bytes)


@pytest.mark.parametrize(
    "path",
    [OnclusivePath.from_relative("tests/integration/data/test_files/file2.py")],
)
def test_open_string(localfs, path):
    """Test open."""
    with localfs.open(path) as f:
        assert isinstance(f.read(), str)


@pytest.mark.parametrize(
    "path, expected",
    [
        (
            OnclusivePath.from_relative("tests/integration/data/test_files"),
            [
                OnclusivePath.from_relative(
                    "tests/integration/data/test_files/file1.md"
                ),
                OnclusivePath.from_relative(
                    "tests/integration/data/test_files/file2.py"
                ),
                OnclusivePath.from_relative("tests/integration/data/test_files/file3"),
            ],
        )
    ],
)
def test_ls(localfs, path, expected):
    """Test open."""
    assert localfs.ls(path) == expected


@pytest.mark.parametrize(
    "path",
    [OnclusivePath.from_relative("tests/integration/data/test_files/new")],
)
def test_mkdir(localfs, path):
    """Test open."""
    assert not localfs.exists(path)
    localfs.mkdir(path)
    assert localfs.exists(path)
    localfs.rm(path)


@pytest.mark.parametrize(
    "path",
    [OnclusivePath.from_relative("tests/integration/data/directory/subdirectory")],
)
def test_mkdirs(localfs, path):
    """Test open."""
    assert not localfs.exists(path)
    localfs.mkdirs(path)
    assert localfs.exists(path)
    assert localfs.exists(path.parent)
    localfs.rm(path.parent)


@pytest.mark.parametrize(
    "source, destination",
    [
        (
            OnclusivePath.from_relative("tests/integration/data/test_files"),
            OnclusivePath.from_relative("tests/integration/data/test_files_copy"),
        )
    ],
)
def test_cp(localfs, source, destination):
    """Test cp method."""
    assert localfs.exists(source)
    assert not localfs.exists(destination)
    localfs.cp(source, destination)
    assert localfs.exists(destination)
    localfs.rm(destination)


@pytest.mark.parametrize(
    "glob, expected",
    [
        (
            OnclusivePath.from_relative("tests/integration/data/test_files/*"),
            [
                OnclusivePath.from_relative(
                    "tests/integration/data/test_files/file1.md"
                ),
                OnclusivePath.from_relative(
                    "tests/integration/data/test_files/file2.py"
                ),
                OnclusivePath.from_relative("tests/integration/data/test_files/file3"),
            ],
        )
    ],
)
def test_glob(localfs, glob, expected):
    """Test blog method."""
    assert localfs.glob(glob) == expected


@pytest.mark.parametrize(
    "path, expected",
    [
        (
            OnclusivePath.from_relative("tests/integration/data/test_files/file1.md"),
            True,
        ),
        (
            OnclusivePath.from_relative("tests/integration/data/test_files/file4.toml"),
            False,
        ),
    ],
)
def test_exists(localfs, path, expected):
    """Test exists method."""
    assert localfs.exists(path) == expected


@pytest.mark.parametrize(
    "path, expected",
    [
        (
            OnclusivePath.from_relative("tests/integration/data/test_files/file2.py"),
            True,
        ),
        (OnclusivePath.from_relative("tests/integration/data/test_files"), False),
    ],
)
def test_isfile(localfs, path, expected):
    """Test isfile method."""
    assert localfs.isfile(path) == expected


@pytest.mark.parametrize(
    "path, expected",
    [
        (
            OnclusivePath.from_relative("tests/integration/data/test_files/file2.py"),
            False,
        ),
        (OnclusivePath.from_relative("tests/integration/data/test_files"), True),
    ],
)
def test_isdir(localfs, path, expected):
    """Test isdir method."""
    assert localfs.isdir(path) == expected


@pytest.mark.parametrize(
    "path, expected",
    [
        (OnclusivePath.from_relative("tests/integration/data"), False),
        (OnclusivePath.from_relative("tests/integration/data/test_files/*"), True),
    ],
)
def test_isglob(localfs, path, expected):
    """Test isglob method."""
    assert localfs.isglob(path) == expected


@pytest.mark.parametrize(
    "path",
    [OnclusivePath.from_relative("tests/integration/data/test_files/file2.py")],
)
def test_info(localfs, path):
    """Test info method."""
    info = localfs.info(path)

    assert isinstance(info.size, int)
    assert isinstance(info.path, str)
    assert isinstance(info.created, datetime.datetime)
    assert isinstance(info.last_modified, datetime.datetime)
