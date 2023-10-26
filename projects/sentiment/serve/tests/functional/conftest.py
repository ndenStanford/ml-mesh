"""Conftest."""

# Standard Library
import json

# 3rd party libraries
import pytest
from requests_toolbelt.sessions import BaseUrlSession

# Internal libraries
from onclusiveml.serving.rest.serve import ServingParams

# Source
from src.serve.artifacts import ServedModelArtifacts


@pytest.fixture
def test_client():
    """Test client fixture.

    Client-like session with base url to avoid duplication, as per
    https://toolbelt.readthedocs.io/en/latest/sessions.html#baseurlsession
    """
    serving_params = ServingParams()
    model_server_port = serving_params.uvicorn_settings.http_port
    test_model_server_url = f"http://serve:{model_server_port}"

    return BaseUrlSession(base_url=test_model_server_url)


@pytest.fixture
def test_served_model_artifacts():
    """Served model artifacts."""
    return ServedModelArtifacts()


@pytest.fixture
def test_model_name(test_served_model_artifacts):
    """Model name fixture."""
    return test_served_model_artifacts.model_name


@pytest.fixture
def test_inputs(test_served_model_artifacts):
    """Inputs fixture."""
    with open(test_served_model_artifacts.inputs_test_file, "r") as json_file:
        test_inputs = json.load(json_file)

    return test_inputs


@pytest.fixture
def test_inference_params(test_served_model_artifacts):
    """Inference parameters fixture."""
    with open(test_served_model_artifacts.inference_params_test_file, "r") as json_file:
        test_inference_params = json.load(json_file)

    return test_inference_params


@pytest.fixture
def test_predictions(test_served_model_artifacts):
    """Prediction tests fixture."""
    with open(test_served_model_artifacts.predictions_test_file, "r") as json_file:
        test_predictions = json.load(json_file)

    return test_predictions


@pytest.fixture
def test_model_card(test_served_model_artifacts):
    """Model card fixture."""
    with open(test_served_model_artifacts.model_card_file, "r") as json_file:
        test_model_card = json.load(json_file)

    return test_model_card


@pytest.fixture
def test_atol() -> float:
    """Test absolute error for float comparison."""
    return 2e-02


@pytest.fixture
def test_rtol() -> float:
    """Test relative error for float comparison."""
    return 1e-02
