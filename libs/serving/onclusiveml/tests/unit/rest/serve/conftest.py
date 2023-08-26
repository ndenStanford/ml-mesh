"""Conftest."""

# 3rd party libraries
import pytest


@pytest.fixture
def test_model_name():
    """Model name fixture."""
    return "test_animal_classifier"
