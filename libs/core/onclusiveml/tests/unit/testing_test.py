"""Test for testing utilities."""

# Standard Library
from functools import lru_cache

# 3rd party libraries
from pydantic import BaseSettings

# Internal libraries
from onclusiveml.core.testing import get_override_settings_context_manager


class TestSettings(BaseSettings):
    debug: bool = False


@lru_cache()
def get_settings():
    return TestSettings()


override_settings = get_override_settings_context_manager(get_settings)


@override_settings(debug=True)
def override_settings_decorator_test():
    """Test override settings"""
    settings = get_settings()
    assert settings.debug is True


def original_settings_test():
    """Test settings original value."""
    settings = get_settings()
    assert settings.debug is False
