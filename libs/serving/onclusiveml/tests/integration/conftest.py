# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.serving.params import ServingParams


@pytest.fixture
def test_configuration():

    return ServingParams().dict()
