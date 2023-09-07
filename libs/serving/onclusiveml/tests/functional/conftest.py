"""Conftests."""

# 3rd party libraries
import pytest


@pytest.fixture
def test_api_version():
    """API version fixture."""
    return "test-version"


@pytest.fixture
def test_port():
    """Port fixture."""
    return 8000


@pytest.fixture
def test_model_name():
    """Model name fixture."""
    return "test-model"


@pytest.fixture
def test_locustfile():
    """Locustfile fixture."""
    return "libs/serving/onclusiveml/tests/integration/rest/testing/test_locustfile.py"
