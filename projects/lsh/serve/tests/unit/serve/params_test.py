# Standard Library
import os

# 3rd party libraries
import pytest

# Source
from src.params import ServedModelParams


@pytest.mark.parametrize(
    "test_remove_prefix_model, test_model_artifact_directory_expected, test_inputs_test_file_expected, test_inference_params_test_file_expected, test_predictions_test_file_expected",  # noqa: E501
    [
        (
            False,
            "./model/some/other/dir",
            "./model/some/other/inputs",
            "./model/some/other/inference_param",
            "./model/some/other/predictions",
        ),
        (
            True,
            "./some/other/dir",
            "./some/other/inputs",
            "./some/other/inference_param",
            "./some/other/predictions",
        ),
    ],
)
def test_lsh_served_model_params():
    """Tests the initialization of the ServedModelParams class"""
    ServedModelParams()


def test_served_model_params_env_prefix():
    """Tests the inherited environment variable prefix (from KeywordsServingBaseParams) of the
    ServedModelParams class"""

    assert ServedModelParams.__config__.env_prefix == "onclusiveml_serving_"


@pytest.mark.parametrize(
    "test_field_name, test_field_value_expected",
    [
        ("model_name", "test_model_name"),
        ("model_directory", "test_dir"),
    ],
)
def test_served_model_params_set_fields_via_env_vars(
    test_field_name, test_field_value_expected
):
    """Tests the correct behaviour of the inherited environment variable prefix (from
    KeywordsServingBaseParams) of the ServedModelParams class's fields by initializing an instance
    after setting the corresponding environment variables in the local test scope."""

    prefixed_field_env_var_ref = f"onclusiveml_serving_{test_field_name}"
    os.environ[prefixed_field_env_var_ref] = test_field_value_expected

    test_keywords_served_model_params = ServedModelParams()

    test_attribute_values_actual = getattr(
        test_keywords_served_model_params, test_field_name
    )
    assert test_attribute_values_actual == test_field_value_expected

    del os.environ[prefixed_field_env_var_ref]
