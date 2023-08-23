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
@pytest.mark.parametrize("test_record_index", [0, 1, 2])
def test_model_server_predict(
    test_model_name,
    test_client,
    test_inputs,
    test_predictions,
    test_record_index,
    test_atol,
    test_rtol,
):
    """Tests the running ModelServer's predict endpoint by making genuine http requests, using the
    custom data models for validation and the test files from the model artifact as ground truth
    for the regression test element."""

    input = PredictRequestModel(
        configuration=PredictConfiguration(language="en"),
        inputs=PredictInputContentModel(content=test_inputs[test_record_index]),
    )

    test_response = test_client.post(
        f"/v1/model/{test_model_name}/predict", json=input.dict()
    )

    assert test_response.status_code == 200
    actual_output = test_response.json()["outputs"]

    expected_output = test_predictions[test_record_index]

    print("actual_output", actual_output)
    print("expected_output", expected_output)
    assert actual_output.get("label") == expected_output.get("label")
    torch.testing.assert_close(
        actual_output.get("positive_prob"),
        expected_output.get("positive_prob"),
        atol=test_atol,
        rtol=test_rtol,
    )
    torch.testing.assert_close(
        actual_output.get("negative_prob"),
        expected_output.get("negative_prob"),
        atol=test_atol,
        rtol=test_rtol,
    )


@pytest.mark.parametrize(
    "test_sample_content, test_sample_entities, test_sample_response",
    [
        (
            "I love John. I hate Jack",
            [{"text": "John"}, {"text": "Jack"}],
            {
                "label": "negative",
                "negative_prob": 0.4735,
                "positive_prob": 0.4508,
                "entities": [
                    {"text": "John", "sentiment": "positive"},
                    {"text": "Jack", "sentiment": "negative"},
                ],
            },
        )
    ],
)
def test_served_sent_model_with_entities_predict(
    test_model_name,
    test_client,
    test_served_model_artifacts,
    test_sample_content,
    test_sample_entities,
    test_sample_response,
):
    """Tests the fully initialized and loaded ServedSentModel's predict method, using the
    custom data models for validation and the test files from the model artifact as ground truth
    for the regression test element."""

    input = PredictRequestModel(
        configuration=PredictConfiguration(
            language="en", entities=test_sample_entities
        ),
        inputs=PredictInputContentModel(content=test_sample_content),
    )

    test_response = test_client.post(
        f"/v1/model/{test_model_name}/predict", json=input.dict()
    )

    assert test_response.status_code == 200
    actual_output = test_response.json()["outputs"]

    assert actual_output.get("entities")[0].get("text") == test_sample_response.get(
        "entities"
    )[0].get("text")
    assert actual_output.get("entities")[0].get(
        "sentiment"
    ) == test_sample_response.get("entities")[0].get("sentiment")


@pytest.mark.order(7)
def test_model_server_bio(test_model_name, test_client, test_model_card):
    """Tests the running ModelServer's bio endpoint by making genuine http requests, using the
    custom data models for validation and the model card from the model artifact as ground truth
    for the regression test element."""

    test_response = test_client.get(f"/v1/model/{test_model_name}/bio")

    assert test_response.status_code == 200
    actual_output = test_response.json()

    expected_output = BioResponseModel(
        model_name=test_model_name, model_card=test_model_card
    ).dict()

    assert actual_output == expected_output
