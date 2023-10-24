"""Conftest."""

# Standard Library
from typing import Any, List

# 3rd party libraries
import pytest
from pydantic import BaseModel

# Internal libraries
from onclusiveml.serving import ServingBaseParams
from onclusiveml.serving.rest.serve import (
    ModelServer,
    ServedModel,
    ServingParams,
)


@pytest.fixture
def test_model_name():
    """Model name fixture."""
    return "test_animal_classifier"


@pytest.fixture
def test_model_server():
    """Test model server."""
    test_serving_params = ServingParams(
        add_liveness=True,
        add_readiness=True,
        add_model_predict=False,
        add_model_bio=False,
        api_version="v1",
    )
    model_server = ModelServer(configuration=test_serving_params)
    return model_server


@pytest.fixture
def test_serving_base_params_env_prefix():
    """Returns the environment prefix of the ServingBaseParams class."""
    return ServingBaseParams.__config__.env_prefix


@pytest.fixture
def get_test_record():
    """Test record fixture."""

    class TestRecord(BaseModel):
        """Test model."""

        number_of_legs: int

    return TestRecord


@pytest.fixture
def get_test_prediction():
    """Test prediction fixture."""

    class TestPrediction(BaseModel):
        """Test model."""

        animal: str

    return TestPrediction


@pytest.fixture
def get_test_predict_request_model(get_test_record):
    """Test prediction fixture."""

    class TestModelPredictRequestModel(BaseModel):
        """Test model."""

        instances: List[get_test_record]

    return TestModelPredictRequestModel


@pytest.fixture
def get_test_served_model(get_test_predict_request_model, get_test_prediction):
    """Test served model fixture."""

    class TestModelPredictResponseModel(BaseModel):
        """Test model."""

        predictions: List[get_test_prediction]

    class TestBioResponseModel(ServedModel.bio_response_model):
        """Bio response model."""

        type: str = "classifier"

    class TestServedModel(ServedModel):
        """A minimal working example of a subclasses custom model for testing purposes."""

        predict_request_model = get_test_predict_request_model
        predict_response_model = TestModelPredictResponseModel
        bio_response_model = TestBioResponseModel

        def predict(
            self, payload: predict_request_model, *args: Any, **kwargs: Any
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
                    predictions.append(get_test_prediction(animal="snake"))
                elif test_record.number_of_legs == 1:
                    predictions.append(get_test_prediction(animal="flamingo"))
                elif test_record.number_of_legs == 2:
                    predictions.append(get_test_prediction(animal="robin"))
                else:
                    predictions.append(get_test_prediction(animal="dog"))

            return self.predict_response_model(predictions=predictions)

        def bio(self) -> bio_response_model:
            """Model meta data method.

            Implements a basic model bio data model using the TestBioResponseModel
            test class.
            """
            return self.bio_response_model(name=self.name)

    return TestServedModel
