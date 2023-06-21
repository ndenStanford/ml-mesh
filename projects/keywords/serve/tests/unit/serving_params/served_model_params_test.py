# Standard Library
import os

# 3rd party libraries
import pytest

# Source
from src.serving_params import ServedModelParams


def test_keywords_served_model_params():
    ServedModelParams()


def test_served_model_params_env_prefix():

    assert ServedModelParams.__config__.env_prefix == "onclusiveml_serving_"


@pytest.mark.parametrize(
    "test_field_name, test_field_value_expected",
    [
        ("model_name", "test_model_name"),
        ("model_artifact_directory", "test_dir"),
        ("model_card_file", "test_model_card"),
        ("inputs_test_file", "test_inputs_location"),
        ("inference_params_test_file", "test_inference_params_location"),
        ("predictions_test_file", "test_predictions_location"),
    ],
)
def test_served_model_params_set_fields_via_env_vars(
    test_field_name, test_field_value_expected
):
    """Check if the prefix inherited from `KeywordsServingBaseParams` works as expected"""

    prefixed_field_env_var_ref = f"onclusiveml_serving_{test_field_name}"
    os.environ[prefixed_field_env_var_ref] = test_field_value_expected

    test_keywords_served_model_params = ServedModelParams()

    test_attribute_values_actual = getattr(
        test_keywords_served_model_params, test_field_name
    )
    assert test_attribute_values_actual == test_field_value_expected

    del os.environ[prefixed_field_env_var_ref]
