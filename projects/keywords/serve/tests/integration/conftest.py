# Standard Library
import json

# 3rd party libraries
import pytest

# Source
from src.serving_params import ServedModelParams


@pytest.fixture
def test_model_name():

    return "test-model"


@pytest.fixture
def test_served_model_params(test_model_name):

    return ServedModelParams(model_name=test_model_name)


@pytest.fixture
def test_inputs(test_served_model_params):

    with open(test_served_model_params.inputs_test_file, "r") as json_file:
        test_inputs = json.load(json_file)

    return test_inputs


@pytest.fixture
def test_inference_params(test_served_model_params):

    with open(test_served_model_params.inference_params_test_file, "r") as json_file:
        test_inference_params = json.load(json_file)

    return test_inference_params


@pytest.fixture
def test_predictions(test_served_model_params):

    with open(test_served_model_params.predictions_test_file, "r") as json_file:
        test_predictions = json.load(json_file)

    return test_predictions


@pytest.fixture
def test_model_card(test_served_model_params):

    with open(test_served_model_params.model_card_file, "r") as json_file:
        test_model_card = json.load(json_file)

    return test_model_card
