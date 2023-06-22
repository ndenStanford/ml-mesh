# Standard Library
import json

# 3rd party libraries
import pytest
from fastapi.testclient import TestClient

# Source
from src.model_server import get_model_server
from src.serving_params import ServedModelArtifacts


@pytest.fixture
def test_served_model_artifacts():

    return ServedModelArtifacts()


@pytest.fixture
def test_model_name(test_served_model_artifacts):

    return test_served_model_artifacts.model_name


@pytest.fixture
def test_inputs(test_served_model_artifacts):

    with open(test_served_model_artifacts.inputs_test_file, "r") as json_file:
        test_inputs = json.load(json_file)

    return test_inputs


@pytest.fixture
def test_inference_params(test_served_model_artifacts):

    with open(test_served_model_artifacts.inference_params_test_file, "r") as json_file:
        test_inference_params = json.load(json_file)

    return test_inference_params


@pytest.fixture
def test_predictions(test_served_model_artifacts):

    with open(test_served_model_artifacts.predictions_test_file, "r") as json_file:
        test_predictions = json.load(json_file)

    return test_predictions


@pytest.fixture
def test_model_card(test_served_model_artifacts):

    with open(test_served_model_artifacts.model_card_file, "r") as json_file:
        test_model_card = json.load(json_file)

    return test_model_card


@pytest.fixture
def test_client():

    model_server = get_model_server()

    return TestClient(model_server)
