# Standard Library
import os

# 3rd party libraries
import pytest

# Source
from src.keywords_serving_params import KeywordsServedModelParams


def test_keywords_served_model_params():
    KeywordsServedModelParams()


def test_keywords_served_model_params_env_prefix():

    assert (
        KeywordsServedModelParams.__config__.env_prefix
        == "onclusiveml_serving_keywords_"  # noqa: W503
    )


@pytest.mark.parametrize(
    "test_field_name, test_field_value_expected",
    [
        ("model_artifact_directory", "test_dir"),
        ("document_pipeline_artifact", "test_document_pipeline"),
        ("word_pipeline_artifact", "test_word_pipeline"),
        ("model_card", "test_model_card"),
    ],
)
def test_keywords_served_model_params_set_fields_via_env_vars(
    test_field_name, test_field_value_expected
):
    """Check if the prefix inherited from `KeywordsServingBaseParams` works as expected"""

    prefixed_field_env_var_ref = f"onclusiveml_serving_keywords_{test_field_name}"
    os.environ[prefixed_field_env_var_ref] = test_field_value_expected

    test_keywords_served_model_params = KeywordsServedModelParams()

    test_attribute_values_actual = getattr(
        test_keywords_served_model_params, test_field_name
    )
    assert test_attribute_values_actual == test_field_value_expected

    del os.environ[prefixed_field_env_var_ref]
