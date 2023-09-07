"""Conftest."""

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.serving import ServingBaseParams


@pytest.fixture
def test_serving_base_params_env_prefix():
    """Returns the environment prefix of the ServingBaseParams class."""
    return ServingBaseParams.__config__.env_prefix
