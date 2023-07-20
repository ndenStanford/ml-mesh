# Standard Library
import builtins
import io
import json
import os

# 3rd party libraries
import pytest

# Source
from src.serving_params import ServedModelArtifacts, ServedModelParams


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
def test_served_model_artifacts(
    test_model_card,
    monkeypatch,
    test_remove_prefix_model,
    test_model_artifact_directory_expected,
    test_inputs_test_file_expected,
    test_inference_params_test_file_expected,
    test_predictions_test_file_expected,
):
    """Tests the constructor method of the ServedModelArtifacts class, mocking up the json.load
    method. In particular, checks for the behaviour of the constructor arg `remove_model_prefix`."""

    def mock_load(json_file):
        return test_model_card

    class MockTextWrapper(object):
        def __init__(self, *args, **kwargs):
            pass

        @staticmethod
        def close():
            pass

    def mock_open(json_file_path):
        return MockTextWrapper

    monkeypatch.setattr(builtins, "open", mock_open)
    monkeypatch.setattr(json, "load", mock_load)
    monkeypatch.setattr(io, "TextIOWrapper", MockTextWrapper)

    served_model_artifacts = ServedModelArtifacts(
        remove_model_prefix=test_remove_prefix_model
    )

    assert (
        served_model_artifacts.model_artifact_directory
        == test_model_artifact_directory_expected  # noqa: W503
    )
    assert served_model_artifacts.inputs_test_file == test_inputs_test_file_expected
    assert (
        served_model_artifacts.inference_params_test_file
        == test_inference_params_test_file_expected  # noqa: W503
    )
    assert (
        served_model_artifacts.predictions_test_file
        == test_predictions_test_file_expected  # noqa: W503
    )


def test_ner_served_model_params():
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

    test_ner_served_model_params = ServedModelParams()

    test_attribute_values_actual = getattr(
        test_ner_served_model_params, test_field_name
    )
    assert test_attribute_values_actual == test_field_value_expected

    del os.environ[prefixed_field_env_var_ref]
