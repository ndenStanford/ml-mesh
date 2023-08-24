# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.serving.rest.serve import (
    LivenessProbeResponse,
    ReadinessProbeResponse,
)

# Source
from src.serve.server_models import (
    PredictConfiguration,
    PredictInputDocumentModel,
    PredictRequestModel,
)


@pytest.mark.order(5)
def test_model_server_root(test_client):
    """Tests the running ModelServer instance's root endpoint by making a genuine http
    request"""

    root_response = test_client.get("/v1/")

    assert root_response.status_code == 200


@pytest.mark.order(6)
def test_model_server_liveness(test_client):
    """Tests the running ModelServer instance's liveness endpoint by making a genuine http
    request"""

    liveness_response = test_client.get("/v1/live")

    assert liveness_response.status_code == 200
    assert liveness_response.json() == LivenessProbeResponse().dict()


@pytest.mark.order(6)
def test_model_server_readiness(test_client):
    """Tests the running ModelServer instance's readiness endpoint by making a genuine http
    request"""

    readiness_response = test_client.get("/v1/ready")

    assert readiness_response.status_code == 200
    assert readiness_response.json() == ReadinessProbeResponse().dict()


@pytest.mark.order(7)
def test_model_server_predict(
    test_model_name,
    test_client,
    test_predict_input,
    test_expected_predict_output,
):
    """Tests the running ModelServer's predict endpoint by making genuine http requests, using the
    custom data models for validation and the test files from the model artifact as ground truth
    for the regression test element."""

    input = PredictRequestModel(
        configuration=PredictConfiguration(),
        inputs=PredictInputDocumentModel(
            content=test_predict_input,
        ),
    )

    test_response = test_client.post(
        f"/v1/model/{test_model_name}/predict", json=input.dict()
    )

    assert test_response.status_code == 200
    test_actual_predict_output = test_response.json()

    assert test_actual_predict_output == test_expected_predict_output.dict()


@pytest.mark.order(7)
def test_model_server_bio(test_model_name, test_client, test_expected_bio_output):
    """Tests the running ModelServer's bio endpoint by making genuine http requests, using the
    custom data models for validation and the model card from the model artifact as ground truth
    for the regression test element."""

    test_response = test_client.get(f"/v1/model/{test_model_name}/bio")

    assert test_response.status_code == 200
    test_actual_bio_output = test_response.json()

    assert test_actual_bio_output == test_expected_bio_output.dict()