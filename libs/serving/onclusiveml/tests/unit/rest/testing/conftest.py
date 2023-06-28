# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.serving.rest.serve import ServingBaseParams


@pytest.fixture
def test_serving_base_params_env_prefix():

    return ServingBaseParams.__config__.env_prefix
