# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.serving import ServingBaseParams


@pytest.fixture
def test_locustfile():
    """The relative path to the locust file needed for the initialization of the LoadTest instance
    when defining client behaviour using the file approach (default)."""

    return "libs/serving/onclusiveml/tests/integration/rest/testing/load_test/test_locustfile.py"


@pytest.fixture
def test_serving_base_params_env_prefix():
    """The environment prefix of the ServingBaseParams base class. Useful for checking the
    environment prefix behaviour of parameter subclasses"""

    return ServingBaseParams.__config__.env_prefix
