"""Artifacts test."""

# Standard Library
import os
from unittest.mock import patch

# 3rd party libraries
import pytest

# Source
from src.serve.artifacts import ServedModelArtifacts


@pytest.mark.parametrize(
    "remove_model_prefix, expected_model_card_file, expected_model_artifact_directory",
    [
        (
            False,
            "models/SUM-TRAINED-79/models/model_card",
            "models/SUM-TRAINED-79/model/some/other/dir",
        ),  # TODO: add a test case for remove_model_prefix=True
    ],
)
@patch("json.loads")
@patch("builtins.open")
def test_served_model_artifacts(
    mock_open,
    mock_json,
    settings,
    model_card,
    remove_model_prefix,
    expected_model_card_file,
    expected_model_artifact_directory,
):
    """Test served model artifact class."""
    mock_json.return_value = model_card

    a = ServedModelArtifacts(settings, remove_model_prefix=remove_model_prefix)

    assert a.model_name == settings.model_name
    assert a.model_directory == settings.model_directory

    mock_open.assert_called_once()
    mock_json.assert_called_once()

    assert a.model_card == model_card

    assert a.inputs_test_file == os.path.join(
        settings.model_directory, model_card["model_test_files"]["inputs"]
    )

    assert a.inference_params_test_file == os.path.join(
        settings.model_directory,
        model_card["model_test_files"]["inference_params"],
    )

    assert a.predictions_test_file == os.path.join(
        settings.model_directory, model_card["model_test_files"]["predictions"]
    )
