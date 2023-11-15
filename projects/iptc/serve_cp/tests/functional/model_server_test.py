"""Model server test."""

# ML libs
import torch

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.serving.rest.serve import (
    LivenessProbeResponse,
    ReadinessProbeResponse,
)

# Source
from src.serve.server_models import (
    BioResponseModel,
    PredictConfiguration,
    PredictInputContentModel,
    PredictRequestModel,
)


@pytest.mark.order(5)
def test_model_server_root(test_client):
    """Tests the running ModelServer instance's root endpoint."""
    root_response = test_client.get("/v1/")
    assert root_response.status_code == 200


@pytest.mark.order(6)
def test_model_server_liveness(test_client):
    """Tests the running ModelServer instance's liveness endpoint."""
    liveness_response = test_client.get("/v1/live")

    assert liveness_response.status_code == 200
    assert liveness_response.json() == LivenessProbeResponse().dict()


@pytest.mark.order(6)
def test_model_server_readiness(test_client):
    """Tests the running ModelServer instance's readiness endpoint."""
    readiness_response = test_client.get("/v1/ready")

    assert readiness_response.status_code == 200
    assert readiness_response.json() == ReadinessProbeResponse().dict()


@pytest.mark.order(7)
@pytest.mark.parametrize("test_record_index", [0, 1])
def test_model_server_predict(
    test_model_name,
    test_client,
    test_inputs,
    test_predictions,
    test_record_index,
    test_atol,
    test_rtol,
):
    """Tests the running ModelServer's predict endpoint by making genuine http requests.

    This test uses the custom data models for validation and the test files from the model
    artifact as ground truth for the regression test element.
    """
    input = PredictRequestModel(
        configuration=PredictConfiguration(),
        inputs=PredictInputContentModel(content=test_inputs[test_record_index]),
    )

    test_response = test_client.post(
        f"/v1/model/{test_model_name}/predict", json=input.dict()
    )

    assert test_response.status_code == 200
    actual_output = test_response.json()["outputs"][0]
    expected_output = test_predictions[test_record_index]

    assert actual_output.get("label") == expected_output.get("label")
    torch.testing.assert_close(
        actual_output.get("score"),
        expected_output.get("score"),
        atol=test_atol,
        rtol=test_rtol,
    )


@pytest.mark.parametrize(
    "test_sample_content, test_sample_response",
    [
        (
            """Stocks reversed earlier losses to close higher despite rising oil prices
            that followed the attack by Hamas on Israel over the weekend. Dovish comments by
            Federal Reserve officials boosted the three major indexes. The Dow Jones Industrial
            Average added nearly 200 points.""",
            {"label": "economy, business and finance", "score": 0.9870237112045288},
        )
    ],
)
def test_served_sent_model_with_iptc_predict(
    test_model_name,
    test_client,
    test_served_model_artifacts,
    test_sample_content,
    test_sample_response,
):
    """Tests the running ModelServer's predict endpoint by making genuine http requests.

    This test the functionality of the endpoint with content input
    """
    input = PredictRequestModel(
        configuration=PredictConfiguration(
            # language="en"
        ),
        inputs=PredictInputContentModel(content=test_sample_content),
    )

    test_response = test_client.post(
        f"/v1/model/{test_model_name}/predict", json=input.dict()
    )

    assert test_response.status_code == 200
    actual_output = test_response.json()["outputs"][0]
    assert actual_output.get("label") == expected_output.get("label")


@pytest.mark.order(7)
def test_model_server_bio(test_model_name, test_client, test_model_card):
    """Tests the running ModelServer's bio endpoint by making genuine http requests.

    This test uses the custom data models for validation and the model card from the model
    artifact as ground truth for the regression test element.
    """
    test_response = test_client.get(f"/v1/model/{test_model_name}/bio")

    assert test_response.status_code == 200
    actual_output = test_response.json()

    expected_output = BioResponseModel(
        model_name=test_model_name, model_card=test_model_card
    ).dict()

    assert actual_output == expected_output
