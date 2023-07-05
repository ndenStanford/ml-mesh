# Standard Library
from typing import List

# 3rd party libraries
import pytest
import requests
from pydantic import BaseModel

# Internal libraries
from onclusiveml.serving.rest.serve import (
    LivenessProbeResponse,
    ModelServer,
    ReadinessProbeResponse,
    ServedModel,
)
from onclusiveml.serving.rest.serve.server_utils import get_model_server_urls
from onclusiveml.serving.rest.serve.serving_params import (
    FastAPISettings,
    ServingParams,
    UvicornSettings,
)


class RootResponse(BaseModel):
    name: str


class TestRecord(BaseModel):

    number_of_legs: int


class TestModelPredictRequestModel(BaseModel):

    instances: List[TestRecord]


class TestPrediction(BaseModel):

    animal: str


class TestModelPredictResponseModel(BaseModel):

    predictions: List[TestPrediction]


class TestBioResponseModel(ServedModel.bio_response_model):

    type: str = "classifier"


class TestServedModel(ServedModel):

    predict_request_model = TestModelPredictRequestModel
    predict_response_model = TestModelPredictResponseModel
    bio_response_model = TestBioResponseModel

    def predict(
        self,
        payload: predict_request_model,
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

        return self.bio_response_model(name=self.name)


# --- server
@pytest.mark.order(1)
@pytest.mark.server
def test_model_server_serve_with_model(test_api_version, test_port, test_model_name):

    test_serving_params = ServingParams(
        add_liveness=True,
        add_readiness=True,
        add_model_predict=True,
        add_model_bio=True,
        api_version=test_api_version,
        fastapi_settings=FastAPISettings(name="test-api"),
        uvicorn_settings=UvicornSettings(http_port=test_port),
    )

    test_model_server = ModelServer(
        configuration=test_serving_params, model=TestServedModel(name=test_model_name)
    )

    test_model_server.serve()


# --- client - root, liveness, readiness
@pytest.mark.order(2)
@pytest.mark.client
@pytest.mark.parametrize(
    "test_url_reference, test_probe_response_model",
    [
        ("root", RootResponse),
        ("liveness", LivenessProbeResponse),
        ("readiness", ReadinessProbeResponse),
    ],
)
def test_model_server_client_no_model(
    test_api_version, test_port, test_url_reference, test_probe_response_model
):
    test_model_server_urls = get_model_server_urls(api_version=test_api_version)

    url = f"http://localhost:{test_port}" + getattr(
        test_model_server_urls, test_url_reference
    )

    response = requests.get(url)

    test_probe_response_model(**response.json())


# --- client - model predict
@pytest.mark.order(4)
@pytest.mark.client
@pytest.mark.parametrize(
    "test_request_data, test_response_model, test_response_expected",
    [
        (
            TestModelPredictRequestModel(
                instances=[
                    TestRecord(number_of_legs=0),
                ]
            ),
            TestModelPredictResponseModel,
            TestModelPredictResponseModel(
                predictions=[
                    TestPrediction(animal="snake"),
                ]
            ),
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
            TestModelPredictResponseModel,
            TestModelPredictResponseModel(
                predictions=[
                    TestPrediction(animal="flamingo"),
                    TestPrediction(animal="robin"),
                    TestPrediction(animal="dog"),
                    TestPrediction(animal="dog"),
                ]
            ),
        ),
    ],
)
def test_model_server_serve_predict(
    test_api_version,
    test_port,
    test_model_name,
    test_request_data,
    test_response_model,
    test_response_expected,
):

    test_model_server_urls = get_model_server_urls(
        api_version=test_api_version, model_name=test_model_name
    )

    model_predict_url = (
        f"http://localhost:{test_port}" + test_model_server_urls.model_predict
    )

    response = requests.post(model_predict_url, json=test_request_data.dict())

    test_response_actual = test_response_model(**response.json())

    assert test_response_actual == test_response_expected


# --- client - model bio
@pytest.mark.order(3)
@pytest.mark.client
@pytest.mark.parametrize(
    "test_response_model",
    [TestBioResponseModel],
)
def test_modeel_server_serve_bio(
    test_api_version,
    test_port,
    test_model_name,
    test_response_model,
):

    test_model_server_urls = get_model_server_urls(
        api_version=test_api_version, model_name=test_model_name
    )

    model_bio_url = f"http://localhost:{test_port}" + test_model_server_urls.model_bio

    response = requests.get(model_bio_url)

    test_response_actual = test_response_model(**response.json())
    test_response_expected = TestBioResponseModel(name=test_model_name)

    assert test_response_actual == test_response_expected
