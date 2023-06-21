# Standard Library
import os

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.serving.rest import (
    FastAPISettings,
    ServingParams,
    UvicornSettings,
)


def test_serving_params():

    ServingParams()


def test_serving_params_env_prefix():
    assert ServingParams.__config__.env_prefix == "onclusiveml_serving_"


@pytest.mark.parametrize(
    "test_subsettings_field", ["uvicorn_settings", "fastapi_settings"]
)
def test_serving_params_env_prefix_nested_settings(test_subsettings_field):
    """Check that the original prefix still applies to nested fields"""
    keyword_serving_params = ServingParams()

    subsettings = getattr(keyword_serving_params, test_subsettings_field)

    assert (
        subsettings.__config__.env_prefix
        == ServingParams.__config__.env_prefix  # noqa: W503
    )


@pytest.mark.parametrize(
    "test_field_name, test_field_value_raw_expected, test_field_value_expected",
    [
        ("add_liveness", "NO", False),  # check all "NO", "No", "n", "N", "False"
        ("add_liveness", "No", False),
        ("add_liveness", "n", False),
        ("add_liveness", "N", False),
        ("add_liveness", "False", False),
        ("add_readiness", "YES", True),  # check all "YES", "Yes", "y", "Y", "True"
        ("add_readiness", "Yes", True),
        ("add_readiness", "y", True),
        ("add_readiness", "Y", True),
        ("add_readiness", "True", True),
        ("add_model_predict", "no", False),
        ("add_model_bio", "no", False),
        (
            "uvicorn_settings",
            UvicornSettings(http_port=9000, host="test_host").json(),
            UvicornSettings(http_port=9000, host="test_host"),
        ),
        (
            "fastapi_settings",
            FastAPISettings(name="test_api_name").json(),
            FastAPISettings(name="test_api_name"),
        ),
    ],
)
def test_serving_params_set_fields_via_env_vars(
    test_field_name, test_field_value_raw_expected, test_field_value_expected
):
    """Check if the prefix inherited from `KeywordsServingBaseParams` works as expected for direct
    fields"""

    prefixed_field_env_var_ref = f"onclusiveml_serving_{test_field_name}"
    os.environ[prefixed_field_env_var_ref] = test_field_value_raw_expected

    test_keywords_serving_params = ServingParams()

    test_attribute_values_actual = getattr(
        test_keywords_serving_params, test_field_name
    )

    assert test_attribute_values_actual == test_field_value_expected

    del os.environ[prefixed_field_env_var_ref]
