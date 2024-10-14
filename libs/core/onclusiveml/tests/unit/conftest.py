"""Conftest."""

# Standard Library
from collections.abc import Iterator

# 3rd party libraries
import pytest
from pytest import FixtureRequest

# Source
from src import Settings, settings


@pytest.fixture
def patch_settings(request: FixtureRequest) -> Iterator[Settings]:
    """Patch settings."""
    # Make a copy of the original settings
    original_settings = settings.model_copy()
    # Collect the env vars to patch
    env_vars_to_patch = getattr(request, "param", {})
    # Patch the settings to use the default values
    for k, v in settings.model_fields.items():
        setattr(settings, k, v.default)
    # Patch the settings with the parametrized env vars
    for key, val in env_vars_to_patch.items():
        # Raise an error if the env var is not defined in the settings
        if not hasattr(settings, key):
            raise ValueError(f"Unknown setting: {key}")
        # Raise an error if the env var has an invalid type
        expected_type = getattr(settings, key).__class__
        if not isinstance(val, expected_type):
            raise ValueError(
                f"Invalid type for {key}: {val.__class__} instead " "of {expected_type}"
            )
        setattr(settings, key, val)

    yield settings
    # Restore the original settings
    settings.__dict__.update(original_settings.__dict__)
