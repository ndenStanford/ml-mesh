"""Prediction schemas tests."""

# Standard Library
from typing import List

# 3rd party libraries
import pytest
from pydantic import BaseModel

# Internal libraries
from onclusiveml.serving.rest.serve import ServedModel


class TestRecord(BaseModel):
    """Test model."""

    number_of_legs: int


class TestPrediction(BaseModel):
    """Test model."""

    animal: str


class TestModelPredictRequestModel(BaseModel):
    """Test model."""

    instances: List[TestRecord]


class TestModelPredictResponseModel(BaseModel):
    """Test model."""

    predictions: List[TestPrediction]


# --- test the ServedModel class
def test_served_model_load(test_model_name):
    """Tests the initialization and loading behaviour of the ServedModel base class."""
    served_model = ServedModel(name=test_model_name)
    # base class `load` behaviour
    assert served_model.ready is not True
    assert served_model.is_ready() is not True

    served_model.load()

    assert served_model.ready is True
    assert served_model.is_ready() is True


def test_served_model_predict(test_model_name):
    """Tests the predict method stump of the ServedModel base class."""
    # get loaded model
    served_model = ServedModel(name=test_model_name)

    served_model.load()
    # call `predict` stump
    test_payload = served_model.predict_request_model(instances=[1, 2])
    served_model.predict(payload=test_payload)


def test_served_model_bio(test_model_name):
    """Tests the bio method stump of the ServedModel base class."""
    served_model = ServedModel(name=test_model_name)
    # call `bio` stump
    served_model_bio_actual = served_model.bio()

    served_model_bio_expected = served_model.bio_response_model(name=test_model_name)

    assert served_model_bio_actual == served_model_bio_expected


# --- test the TestServedModel class
def test_test_served_model_load(test_model_name, get_test_served_model):
    """Tests the initialization and loading behaviour of the subclassed TestServedModel class."""
    test_served_model = get_test_served_model(name=test_model_name)

    assert test_served_model.ready is not True

    test_served_model.load()

    assert test_served_model.ready is True


@pytest.mark.parametrize(
    "test_inputs,test_predictions_expected",
    (
        (
            TestModelPredictRequestModel(
                instances=[
                    TestRecord(number_of_legs=0),
                ]
            ),
            TestModelPredictResponseModel(predictions=[TestPrediction(animal="snake")]),
        ),
        (
            TestModelPredictRequestModel(
                instances=[
                    TestRecord(number_of_legs=1),
                    TestRecord(number_of_legs=2),
                    TestRecord(number_of_legs=4),
                    TestRecord(number_of_legs=10),
                ]
            ),
            TestModelPredictResponseModel(
                predictions=[
                    TestPrediction(animal="flamingo"),
                    TestPrediction(animal="robin"),
                    TestPrediction(animal="dog"),
                    TestPrediction(animal="dog"),
                ]
            ),
        ),
    ),
)
def test_test_served_model_predict(
    test_model_name, test_inputs, test_predictions_expected, get_test_served_model
):
    """Tests the predict method of the subclassed TestServedModel class."""
    # get loaded model
    test_served_model = get_test_served_model(name=test_model_name)

    test_served_model.load()
    # score model & validate outputs
    test_predictions_actual = test_served_model.predict(test_inputs)

    assert test_predictions_actual == test_predictions_expected


def test_test_served_model_bio(test_model_name, get_test_served_model):
    """Tests the bio method of the subclassed TestServedModel class."""
    # get loaded model
    test_served_model = get_test_served_model(name=test_model_name)

    test_served_model.load()

    assert test_served_model.bio() == get_test_served_model.bio_response_model(
        name=test_model_name
    )
