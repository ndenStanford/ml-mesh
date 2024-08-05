"""Conftest."""

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.io import LocalFileSystem
from onclusiveml.io.path import OnclusivePathModule


@pytest.fixture
def pathmodule() -> OnclusivePathModule:
    """Path module fixture."""
    return OnclusivePathModule()


@pytest.fixture
def localfs() -> LocalFileSystem:
    """Path module fixture."""
    return LocalFileSystem()
