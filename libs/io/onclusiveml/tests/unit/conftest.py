"""Conftest."""

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.io.path import OnclusivePathModule


@pytest.fixture
def pathmodule() -> OnclusivePathModule:
    """Path module fixture."""
    return OnclusivePathModule()
