# 3rd party libraries
import pytest

# Internal libraries
from libs.serving.onclusiveml.serving.rest.params import ServingParams


@pytest.fixture
def test_configuration():

    return ServingParams().dict()
