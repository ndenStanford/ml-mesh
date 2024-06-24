"""Model card tests."""

# Standard Library
import os

# 3rd party libraries
import pytest
from pydantic import ValidationError

# Internal libraries
from onclusiveml.tracking.settings import (
    TrackedModelCard,
    TrackedModelSettings,
    TrackedModelTestFiles,
)


@pytest.mark.parametrize(
    "inputs,inference_params,predictions,model_type,model_artifact_attribute_path",
    [
        (
            "inputs",
            "inference_params",
            "predictions",
            "base",
            "artifacts",
        ),
        (
            "inputs",
            "inference_params",
            "predictions",
            "trained",
            "artifacts",
        ),
        (
            "inputs",
            "inference_params",
            "predictions",
            "compiled",
            "artifacts",
        ),
    ],
)
def test_from__init__(
    inputs,
    inference_params,
    predictions,
    model_type,
    model_artifact_attribute_path,
    # model_loader,
):
    """Test initialization."""
    # create model card
    tracked_model_test_files = TrackedModelTestFiles(
        inputs=inputs, inference_params=inference_params, predictions=predictions
    )
    tracked_model_card = TrackedModelCard(
        model_type=model_type,
        model_artifact_attribute_path=model_artifact_attribute_path,
        model_test_files=tracked_model_test_files,
    )
    # TrackedModelCard attributes
    assert (
        tracked_model_card.model_artifact_attribute_path
        == model_artifact_attribute_path  # noqa: W503
    )
    assert tracked_model_card.model_type == model_type
    # TrackedModelTestFiles attributes
    assert tracked_model_card.model_test_files.inputs == inputs
    assert tracked_model_card.model_test_files.inference_params == inference_params
    assert tracked_model_card.model_test_files.predictions == predictions


@pytest.mark.parametrize(
    "project,model,api_token",
    [("a", "b", "c"), ("some project", "some model", "some token")],
)
def test_from_env(project, model, api_token):
    """Test getting parameters from environment variable."""
    for env_name, env_val in (
        ("ONCLUSIVEML_NEPTUNE_PROJECT", project),
        ("ONCLUSIVEML_NEPTUNE_MODEL", model),
        ("ONCLUSIVEML_NEPTUNE_API_TOKEN", api_token),
    ):
        os.environ[env_name] = env_val

    tracked_model_settings = TrackedModelSettings()

    assert tracked_model_settings.project == project
    assert tracked_model_settings.model == model
    # api token needs to be accessed via the SecretString's  `_secret_value` field attribute
    assert tracked_model_settings.api_token._secret_value == api_token
    # clean up env var namespace
    for env_name, env_val in (
        ("ONCLUSIVEML_NEPTUNE_PROJECT", project),
        ("ONCLUSIVEML_NEPTUNE_MODEL", model),
        ("ONCLUSIVEML_NEPTUNE_API_TOKEN", api_token),
    ):
        del os.environ[env_name]


def test_from_empty_env_raise_error():
    """Test from empty env raises error."""
    with pytest.raises(ValidationError):
        TrackedModelSettings()
