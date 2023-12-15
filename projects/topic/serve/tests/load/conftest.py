"""Conftest."""

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
from onclusiveml.serving.serialization.topic.v1 import (
    PredictRequestAttributeSchemaV1,
    PredictRequestParametersSchemaV1,
)

# Source
from src.serve.artifacts import ServedModelArtifacts
from src.serve.schemas import PredictRequestSchema
from src.settings import get_settings


@pytest.fixture(scope="function")
def settings():
    """Settings fixture."""
    return get_settings()


@pytest.fixture
def test_served_model_artifacts(settings):
    """Model artifacts fixture."""
    return ServedModelArtifacts(settings)


@pytest.fixture
def test_model_bio_endpoint_url():
    """Model bio endpoint URL fixture."""
    return "/topic/v1/bio"


@pytest.fixture
def test_model_predict_endpoint_url():
    """Model predict endpoint URL fixture."""
    return "/topic/v1/predict"


@pytest.fixture
def test_inputs(test_served_model_artifacts):
    """Inputs fixture."""
    with open(test_served_model_artifacts.inputs_test_file, "r") as json_file:
        test_inputs = json.load(json_file)

    return test_inputs


@pytest.fixture
def test_model_bio_user(test_model_bio_endpoint_url):
    """Test model bio user."""

    class ModelBioUser(HttpUser):
        """Model bio user."""

        wait_time = between(0.1, 0.3)

        @task()
        def get_model_bio(self):
            """Makes a GET type request against the served model's bio endpoint."""
            self.client.get(test_model_bio_endpoint_url)

    return ModelBioUser


@pytest.fixture
def test_model_predict_user(settings, test_inputs, test_model_predict_endpoint_url):
    """Test model predict user."""

    class ModelPredictUser(HttpUser):
        """Model predict user."""

        # assemble & attach list of sample payloads for model predict endpoint requests
        sample_payloads: List[PredictRequestSchema] = []
        for test_record_index in range(len(test_inputs)):
            sample_payload = PredictRequestSchema.from_data(
                namespace=settings.model_name,
                parameters=PredictRequestParametersSchemaV1(language="en"),
                attributes=PredictRequestAttributeSchemaV1(
                    content=test_inputs[test_record_index]
                ),
            )
            sample_payloads.append(sample_payload)

        @task()
        def get_model_prediction(self):
            """Makes a POST type prediction request to the served model's `predict` endpoint."""
            # randomly sample a payload
            payload = random.choice(self.sample_payloads)

            self.client.post(test_model_predict_endpoint_url, json=payload.dict())

    return ModelPredictUser


@pytest.fixture
def test_load_test_settings(test_model_bio_user, test_model_predict_user):
    """Load test settings fixture."""
    return LoadTestingParams(
        user_classes=[test_model_bio_user, test_model_predict_user],
        locustfile="",
    )


@pytest.fixture
def test_model_criteria(test_model_bio_endpoint_url, test_model_predict_endpoint_url):
    """Load test criteria features."""
    # --- .../bio
    # <= 10 ms latency
    model_bio_latency_crit = Criterion(
        name=ValidMeasurements.avg_response_time.value,
        threshold=10,
        endpoint_type="GET",
        endpoint_url=test_model_bio_endpoint_url,
        ensure_lower=True,
        hard=True,
    )

    # >= 100 requests sent
    model_bio_total_reqs_crit = Criterion(
        name=ValidMeasurements.requests_total.value,
        threshold=100,
        endpoint_type="GET",
        endpoint_url=test_model_bio_endpoint_url,
        ensure_lower=False,
        hard=True,
    )

    # no failures
    model_bio_failure_crit = Criterion(
        name=ValidMeasurements.failures_total.value,
        threshold=1,
        endpoint_type="GET",
        endpoint_url=test_model_bio_endpoint_url,
        ensure_lower=True,
        hard=True,
    )

    # --- .../predict
    # <= 150 ms latency
    model_predict_latency_crit = Criterion(
        name=ValidMeasurements.avg_response_time.value,
        threshold=150,
        endpoint_type="POST",
        endpoint_url=test_model_predict_endpoint_url,
        ensure_lower=True,
        hard=True,
    )

    # >= 100 requests sent
    model_predict_total_reqs_criterion = Criterion(
        name=ValidMeasurements.requests_total.value,
        threshold=100,
        endpoint_type="POST",
        endpoint_url=test_model_predict_endpoint_url,
        ensure_lower=False,
        hard=True,
    )

    # no failures
    model_predict_failure_crit = Criterion(
        name=ValidMeasurements.failures_total.value,
        threshold=1,
        endpoint_type="POST",
        endpoint_url=test_model_predict_endpoint_url,
        ensure_lower=True,
        hard=True,
    )

    return [
        model_bio_latency_crit,
        model_bio_total_reqs_crit,
        model_bio_failure_crit,
        model_predict_latency_crit,
        model_predict_total_reqs_criterion,
        model_predict_failure_crit,
    ]
