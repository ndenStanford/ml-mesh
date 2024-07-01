"""Parameter tests."""

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.serving import ServingBaseParams
from onclusiveml.serving.rest.serve import (
    BetterStackSettings,
    FastAPISettings,
    ServingParams,
    UvicornSettings,
)


@pytest.mark.parametrize(
    "settings_class",
    [
        ServingBaseParams,
        FastAPISettings,
        UvicornSettings,
        BetterStackSettings,
        ServingParams,
    ],
)
def test_settings___init__(settings_class):
    """Tests the initialization of all serving.rest settings/params classes with default values."""
    settings_class()


def test_better_stack_settings_full_url():
    """Tests the BetterStackSettings class' construction of the full_url attribute."""
    better_stack_settings = BetterStackSettings(
        enable=True, api_token="test_token", base_url="test_url/"
    )

    assert better_stack_settings.full_url == "test_url/test_token"
