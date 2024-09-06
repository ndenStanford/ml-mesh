"""Constants test."""

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.io.constants import IOScheme


@pytest.mark.parametrize(
    "enum, expected",
    [
        (IOScheme.FILE, "file://"),
        (IOScheme.GITHUB, "github://"),
        (IOScheme.NEPTUNE, "neptune://"),
        (IOScheme.S3, "s3://"),
        (IOScheme.EFS, "efs://"),
    ],
)
def test_ioscheme_str(enum, expected):
    """Test ioscheme string conversion."""
    assert str(enum) == expected
