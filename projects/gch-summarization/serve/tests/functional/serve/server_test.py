"""Server functional tests."""

# 3rd party libraries
import pytest
import requests

# Internal libraries
from onclusiveml.serving.rest.serve import (
    LivenessProbeResponse,
    ReadinessProbeResponse,
)


def test_model_server_root():
    """Tests the root endpoint of a ModelServer (not running) instance."""
    root_response = requests.get("http://serve:8001/gch-summarization/v1/")

    assert root_response.status_code == 200


def test_model_server_liveness():
    """Tests the liveness endpoint of a ModelServer (not running) instance."""
    liveness_response = requests.get("http://serve:8001/gch-summarization/v1/live")

    assert liveness_response.status_code == 200
    assert liveness_response.json() == LivenessProbeResponse().dict()


def test_model_server_readiness():
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    readiness_response = requests.get("http://serve:8001/gch-summarization/v1/ready")

    assert readiness_response.status_code == 200
    assert readiness_response.json() == ReadinessProbeResponse().dict()


def test_model_server_bio():
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    readiness_response = requests.get("http://serve:8001/gch-summarization/v1/bio")

    assert readiness_response.status_code == 200
    assert readiness_response.json()["data"]["attributes"].get("model_card") is not None


@pytest.mark.parametrize(
    "payload, expected_response",
    [
        (
            {
                "data": {
                    "namespace": "gch-summarization",
                    "attributes": {
                        "content": "Sky News announces slate of special programming for the appointment of the UK's new \
Prime Minister.\nSky News' political programming will expand ahead of a momentous week \
in UK politics with the impending announcement of the new Prime Minister. Sky News' key \
political programmes will return to bring audiences in-depth discussion and analysis of \
all the latest news with live coverage from Downing Street and Westminster.\nHead of Sky \
News, John Ryley:\n'This is a momentous week in British politics, where a new Prime Minister \
will take on an in-tray bursting with crunch decisions.",
                    },
                    "parameters": {
                        "language": "en",
                    },
                }
            },
            {
                "version": 1,
                "data": {
                    "identifier": None,
                    "namespace": "gch-summarization",
                    "attributes": {
                        "summary": "Sky News to expand political programming ahead of the appointment of the new Prime \
Minister. Key political programmes will return to bring audiences in-depth discussion and analysis."
                    },
                },
            },
        )
    ],
)
def test_model_server_prediction(payload, expected_response):
    """Tests predict endpoint of the gch summarization ModelServer."""
    response = requests.post(
        "http://serve:8001/gch-summarization/v1/predict",
        json=payload,
    )

    assert response.status_code == 200
    # TODO: assert score close to expected
    assert response.json() == expected_response
