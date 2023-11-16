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
    root_response = requests.get("http://serve:8000/iptc/v1/")

    assert root_response.status_code == 200


def test_model_server_liveness():
    """Tests the liveness endpoint of a ModelServer (not running) instance."""
    liveness_response = requests.get("http://serve:8000/iptc/v1/live")

    assert liveness_response.status_code == 200
    assert liveness_response.json() == LivenessProbeResponse().dict()


def test_model_server_readiness():
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    readiness_response = requests.get("http://serve:8000/iptc/v1/ready")

    assert readiness_response.status_code == 200
    assert readiness_response.json() == ReadinessProbeResponse().dict()


def test_model_server_bio():
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    readiness_response = requests.get("http://serve:8000/iptc/v1/bio")

    assert readiness_response.status_code == 200
    assert readiness_response.json()["data"]["attributes"].get("model_card") is not None


@pytest.mark.parametrize(
    "payload, expected_response",
    [
        (
            {
                "data": {
                    "identifier": None,
                    "namespace": "iptc",
                    "attributes": {"content": ""},
                    "parameters": {},
                }
            },
            {
                "version": 1,
                "data": {
                    "identifier": None,
                    "namespace": "iptc",
                    "attributes": {"iptc": []},
                },
            },
        ),
        (
            {
                "data": {
                    "namespace": "iptc",
                    "attributes": {
                        "content": """Stocks reversed earlier losses to close higher despite rising oil prices
            that followed the attack by Hamas on Israel over the weekend. Dovish comments by
            Federal Reserve officials boosted the three major indexes. The Dow Jones Industrial
            Average added nearly 200 points."""
                    },
                    "parameters": {},
                }
            },
            {
                "version": 1,
                "data": {
                    "identifier": None,
                    "namespace": "iptc",
                    "attributes": {
                        "iptc": [
                            {"label": "economy, business and finance", "score": 0.9871}
                        ]
                    },
                },
            },
        ),
    ],
)
def test_model_server_prediction(payload, expected_response):
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    response = requests.post(
        "http://serve:8000/iptc/v1/predict",
        json=payload,
    )

    assert response.status_code == 200
    # TODO: assert score close to expected
    iptc = response.json()
    if len(iptc["data"]["attributes"]["iptc"]) != 0:
        iptc["data"]["attributes"]["iptc"] = [
            response.json()["data"]["attributes"]["iptc"][0]
        ]
    assert iptc == expected_response
