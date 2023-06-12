# Standard Library
from typing import Any, List

# 3rd party libraries
import pytest
from pydantic import BaseModel

# Internal libraries
from onclusiveml.serving.rest.serve import ServedModel


class TestRecord(BaseModel):

    number_of_legs: int


class TestModelPredictRequestModel(BaseModel):

    instances: List[TestRecord]


class TestPrediction(BaseModel):

    animal: str


class TestModelPredictResponseModel(BaseModel):

    predictions: List[TestPrediction]


class TestBioResponseModel(BaseModel):

    model_name: str = "ANIMAL-CLASSIFIER-TEST"
    model_type: str = "classifier"


class TestServedModel(ServedModel):

    name: str = "test_animal_classifier"

    predict_request_model = TestModelPredictRequestModel
    predict_response_model = TestModelPredictResponseModel
    bio_response_model = TestBioResponseModel

    bio_response_model = TestBioResponseModel

    def predict(
        self, payload: predict_request_model, *args: Any, **kwargs: Any
    ) -> predict_response_model:
        """Inference method."""

        predictions = []

        for test_record in payload.instances:
            if test_record.number_of_legs == 0:
                predictions.append(TestPrediction(animal="snake"))
            elif test_record.number_of_legs == 1:
                predictions.append(TestPrediction(animal="flamingo"))
            elif test_record.number_of_legs == 2:
                predictions.append(TestPrediction(animal="robin"))
            else:
                predictions.append(TestPrediction(animal="dog"))

        return self.predict_response_model(predictions=predictions)

    def bio(self) -> bio_response_model:

        return self.bio_response_model()


# --- test the ServedModel class
def test_served_model_load(test_model_name):

    served_model = ServedModel(name=test_model_name)
    # base class `load` behaviour
    assert served_model.ready is not True
    assert served_model.is_ready() is not True

    served_model.load()

    assert served_model.ready is True
    assert served_model.is_ready() is True


def test_served_model_predict(test_model_name):
    # get loaded model
    served_model = ServedModel(name=test_model_name)

    served_model.load()
    # call `predict` stump
    request_arg = served_model.predict_request_model(instances=[1, 2])
    some_arg = 1
    some_kwarg = 2
    served_model.predict(request_arg, some_arg, some_kwarg=some_kwarg)


def test_served_model_bio(test_model_name):

    served_model = ServedModel(name=test_model_name)
    # call `bio` stump
    served_model.bio()


# --- test the TestServedModel class
def test_test_served_model_load(test_model_name):

    test_served_model = TestServedModel(name=test_model_name)

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
    test_model_name, test_inputs, test_predictions_expected
):
    # get loaded model
    test_served_model = TestServedModel(name=test_model_name)

    test_served_model.load()
    # score model & validate outputs
    test_predictions_actual = test_served_model.predict(test_inputs)

    assert test_predictions_actual == test_predictions_expected


def test_test_served_model_bio(test_model_name):
    # get loaded model
    test_served_model = TestServedModel(name=test_model_name)

    test_served_model.load()

    assert test_served_model.bio() == TestServedModel.bio_response_model()
