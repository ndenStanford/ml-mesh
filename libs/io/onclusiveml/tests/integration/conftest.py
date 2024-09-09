"""Conftest."""

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.io import LocalFileSystem


@pytest.fixture
def localfs() -> LocalFileSystem:
    """Path module fixture."""
    return LocalFileSystem()
