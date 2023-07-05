# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.serving.rest.serve import ServingBaseParams


@pytest.fixture
def test_serving_base_params_env_prefix():
    """Importing the ServingBaseParams environment prefix to be used a ground truth for subclasses'
    environment prefix tests"""

    return ServingBaseParams.__config__.env_prefix
