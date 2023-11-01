"""Conftests."""

# Standard Library
from typing import List

# 3rd party libraries
import pytest
from pydantic import BaseModel

# Internal libraries
from libs.serving.onclusiveml.serving.rest.serve.params import (
    BetterStackSettings,
    FastAPISettings,
    ServingParams,
    UvicornSettings,
)
from onclusiveml.serving.rest.serve import ModelServer, ServedModel


TEST_API_VERSION = "test-version"
TEST_PORT = 8000
TEST_MODEL_NAME = "test-model"
TEST_APP = "libs.serving.onclusiveml.tests.functional.conftest:TEST_MODEL_SERVER"


@pytest.fixture
def test_api_version():
    """API version fixture."""
    return TEST_API_VERSION


@pytest.fixture
def test_port():
    """Port fixture."""
    return TEST_PORT


@pytest.fixture
def test_model_name():
    """Model name fixture."""
    return TEST_MODEL_NAME


class RootResponse(BaseModel):
    """Root response."""

    name: str


class TestRecord(BaseModel):
    """Test record."""

    number_of_legs: int


class TestModelPredictRequestModel(BaseModel):
    """Test model predict request model."""

    instances: List[TestRecord]


class TestPrediction(BaseModel):
    """Test prediction."""

    animal: str


class TestModelPredictResponseModel(BaseModel):
    """Test model predict response model."""

    predictions: List[TestPrediction]


class TestBioResponseModel(ServedModel.bio_response_model):
    """Test bio response model."""

    type: str = "classifier"


class TestServedModel(ServedModel):
    """A minimal working example of a subclasses custom model for testing purposes."""

    predict_request_model = TestModelPredictRequestModel
    predict_response_model = TestModelPredictResponseModel
    bio_response_model = TestBioResponseModel

    def predict(
        self,
        payload: predict_request_model,
    ) -> predict_response_model:
        """Inference method.

        Implements a very basic animal classifier using the
            - TestModelPredictRequestModel and
            - TestModelPredictResponseModel
        test classes.
        """
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
        """Model meta data method. Implements a basic model bio data model."""
        return self.bio_response_model(name=self.name)


test_serving_params = ServingParams(
    add_liveness=True,
    add_readiness=True,
    add_model_predict=True,
    add_model_bio=True,
    api_version=TEST_API_VERSION,
    fastapi_settings=FastAPISettings(name="test-api"),
    uvicorn_settings=UvicornSettings(port=TEST_PORT, app=TEST_APP),
    betterstack_settings=BetterStackSettings(enable=True),
)

TEST_MODEL_SERVER = ModelServer(
    configuration=test_serving_params, model=TestServedModel(name=TEST_MODEL_NAME)
)


@pytest.fixture
def test_model_server():
    """Test model server fixture."""
    return TEST_MODEL_SERVER
