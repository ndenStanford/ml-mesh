# Standard Library
import builtins
import io
import json

# 3rd party libraries
import pytest

# Source
from src.serving_params import ServedModelArtifacts


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
