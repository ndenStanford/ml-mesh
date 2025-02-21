"""Conftests."""

# Standard Library
import json

# 3rd party libraries
import pytest
from requests_toolbelt.sessions import BaseUrlSession

# Internal libraries
from onclusiveml.serving.rest.serve import ServingParams

# Source
from src.serve.params import ServedModelArtifacts


@pytest.fixture
def test_serving_params():
    """Serving params fixture."""
    return ServingParams()


@pytest.fixture
def test_client(test_serving_params):
    """Client-like session with base url to avoid duplication.

    Reference:
        https://toolbelt.readthedocs.io/en/latest/sessions.html#baseurlsession
    """
    test_model_server_url = f"http://serve:{test_serving_params.uvicorn_settings.port}"

    return BaseUrlSession(base_url=test_model_server_url)


@pytest.fixture
def test_served_model_artifacts():
    """Served model artifacts fixture."""
    return ServedModelArtifacts()


@pytest.fixture
def test_model_name(test_served_model_artifacts):
    """Test model name."""
    return test_served_model_artifacts.model_name


@pytest.fixture
def test_inputs(test_served_model_artifacts):
    """Test inputs."""
    with open(test_served_model_artifacts.inputs_test_file, "r") as json_file:
        test_inputs = json.load(json_file)

    return test_inputs


@pytest.fixture
def test_inference_params(test_served_model_artifacts):
    """Test inference parameters."""
    with open(test_served_model_artifacts.inference_params_test_file, "r") as json_file:
        test_inference_params = json.load(json_file)

    return test_inference_params


@pytest.fixture
def test_predictions(test_served_model_artifacts):
    """Test predictions."""
    with open(test_served_model_artifacts.predictions_test_file, "r") as json_file:
        test_predictions = json.load(json_file)

    return test_predictions


@pytest.fixture
def test_model_card(test_served_model_artifacts):
    """Test model card."""
    with open(test_served_model_artifacts.model_card_file, "r") as json_file:
        test_model_card = json.load(json_file)

    return test_model_card
