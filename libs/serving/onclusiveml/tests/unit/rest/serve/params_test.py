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
    "settings_class, expected_env_prefix",
    [
        (ServingBaseParams, "onclusiveml_serving_"),
        (FastAPISettings, "onclusiveml_serving_fastapi_"),
        (UvicornSettings, "onclusiveml_serving_uvicorn_"),
        (BetterStackSettings, "onclusiveml_serving_betterstack_"),
        (ServingParams, "onclusiveml_serving_"),
    ],
)
def test_settings_env_prefix(settings_class, expected_env_prefix):
    """Tests the environment prefixes for all serving.rest settings/params classes"""

    assert settings_class.Config.env_prefix == expected_env_prefix


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
    """Tests the initialization of all serving.rest settings/params classes with default values"""

    settings_class()


def test_better_stack_settings_full_url():
    """Tests the BetterStackSettings class' construction of the full_url attribute"""

    better_stack_settings = BetterStackSettings(
        enable=True, api_token="test_token", base_url="test_url/"
    )

    assert better_stack_settings.full_url == "test_url/test_token"
