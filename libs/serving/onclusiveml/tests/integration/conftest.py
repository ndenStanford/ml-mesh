# 3rd party libraries
import pytest


@pytest.fixture
def test_api_version():

    return "test-version"


@pytest.fixture
def test_port():

    return 8000


@pytest.fixture
def test_model_name():

    return "test-model"
