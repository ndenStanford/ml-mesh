# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.serving.rest.serve import ServingBaseParams


@pytest.fixture
def test_locustfile():

    return "libs/serving/onclusiveml/tests/integration/rest/testing/test_locustfile.py"


@pytest.fixture
def test_serving_base_params_env_prefix():

    return ServingBaseParams.__config__.env_prefix
