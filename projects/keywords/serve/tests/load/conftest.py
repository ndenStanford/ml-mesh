# Standard Library
import json
import random
from typing import List

# 3rd party libraries
import pytest
from locust import HttpUser, between, task

# Internal libraries
from onclusiveml.serving.rest.testing.load_test import (
    Criterion,
    LoadTestingParams,
    ValidMeasurements,
)

# Source
from src.server_models import (
    PredictConfiguration,
    PredictInputDocumentModel,
    PredictRequestModel,
)
from src.serving_params import ServedModelArtifacts


@pytest.fixture
def test_served_model_artifacts():

    return ServedModelArtifacts()


@pytest.fixture
def test_model_name(test_served_model_artifacts):

    return test_served_model_artifacts.model_name


@pytest.fixture
def test_model_bio_endpoint_url(test_model_name):

    return f"/v1/model/{test_model_name}/bio"


@pytest.fixture
def test_model_predict_endpoint_url(test_model_name):

    return f"/v1/model/{test_model_name}/predict"


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
def test_model_bio_user(test_model_bio_endpoint_url):
    class ModelBioUser(HttpUser):

        wait_time = between(0.1, 0.3)

        @task()
        def get_model_bio(self):
            """
            Makes a GET type request against the served model's bio endpoint
            """
            self.client.get(test_model_bio_endpoint_url)

    return ModelBioUser


@pytest.fixture
def test_model_predict_user(
    test_inputs, test_inference_params, test_model_predict_endpoint_url
):
    class ModelPredictUser(HttpUser):
        # assemble & attach list of sample payloads for model predict endpoint requests
        sample_payloads: List[PredictRequestModel] = []

        for test_record_index in range(len(test_inputs)):
            sample_payload = input = PredictRequestModel(
                configuration=PredictConfiguration(**test_inference_params),
                inputs=[
                    PredictInputDocumentModel(document=test_inputs[test_record_index])
                ],
            )

            sample_payloads.append(sample_payload)

        @task()
        def get_model_prediction(self):
            """
            Makes a POST type prediction request to the served model's `predict` endpoint, using a
            randomly sampled model test record
            """
            # randomly sample a payload
            payload = random.choice(self.sample_payloads)

            self.client.post(test_model_predict_endpoint_url, json=payload.dict())

    return ModelPredictUser


@pytest.fixture
def test_load_test_settings(test_model_bio_user, test_model_predict_user):

    return LoadTestingParams(
        user_classes=[test_model_bio_user, test_model_predict_user],
        locustfile="",
    )


@pytest.fixture
def test_model_criteria(test_model_bio_endpoint_url, test_model_predict_endpoint_url):

    model_bio_latency_crit = Criterion(
        name=ValidMeasurements.avg_response_time.value,
        threshold=10,
        endpoint_type="GET",
        endpoint_url=test_model_bio_endpoint_url,
        ensure_lower=True,
        hard=True,
    )

    model_bio_total_reqs_crit = Criterion(
        name=ValidMeasurements.requests_total.value,
        threshold=100,
        endpoint_type="GET",
        endpoint_url=test_model_bio_endpoint_url,
        ensure_lower=False,
        hard=True,
    )

    model_predict_latency_crit = Criterion(
        name=ValidMeasurements.avg_response_time.value,
        threshold=500,
        endpoint_type="POST",
        endpoint_url=test_model_predict_endpoint_url,
        ensure_lower=True,
        hard=True,
    )

    model_predict_total_reqs_criterion = Criterion(
        name=ValidMeasurements.requests_total.value,
        threshold=50,
        endpoint_type="POST",
        endpoint_url=test_model_predict_endpoint_url,
        ensure_lower=False,
        hard=True,
    )

    return [
        model_bio_latency_crit,
        model_bio_total_reqs_crit,
        model_predict_latency_crit,
        model_predict_total_reqs_criterion,
    ]
