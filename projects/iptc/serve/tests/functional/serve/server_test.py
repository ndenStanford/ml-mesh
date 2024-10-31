"""Server functional tests."""

# 3rd party libraries
import pytest
import requests

# Internal libraries
from onclusiveml.serving.rest.serve import (
    LivenessProbeResponse,
    ReadinessProbeResponse,
)


def test_model_server_liveness():
    """Tests the liveness endpoint of a ModelServer (not running) instance."""
    liveness_response = requests.get("http://serve:8000/iptc-00000000/v1/live")

    assert liveness_response.status_code == 200
    assert liveness_response.json() == LivenessProbeResponse().model_dump()


def test_model_server_readiness():
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    readiness_response = requests.get("http://serve:8000/iptc-00000000/v1/ready")

    assert readiness_response.status_code == 200
    assert readiness_response.json() == ReadinessProbeResponse().model_dump()


def test_model_server_bio():
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    readiness_response = requests.get("http://serve:8000/iptc-00000000/v1/bio")

    assert readiness_response.status_code == 200
    assert readiness_response.json()["data"]["attributes"].get("model_card") is not None


@pytest.mark.parametrize(
    "payload, expected_response",
    [
        (
            {
                "data": {
                    "identifier": None,
                    "namespace": "iptc-00000000",
                    "attributes": {"content": ""},
                    "parameters": {},
                }
            },
            {
                "version": 1,
                "data": {
                    "identifier": None,
                    "namespace": "iptc-00000000",
                    "attributes": {"iptc": []},
                },
            },
        ),
        (
            {
                "data": {
                    "namespace": "iptc-00000000",
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
                    "namespace": "iptc-00000000",
                    "attributes": {
                        "iptc": [
                            {"label": "economy, business and finance", "score": 0.983},
                            {"label": "conflict, war and peace", "score": 0.008},
                            {"label": "politics", "score": 0.0025},
                            {"label": "crime, law and justice", "score": 0.0009},
                            {
                                "label": "arts, culture, entertainment and media",
                                "score": 0.0007,
                            },
                            {"label": "health", "score": 0.0007},
                            {"label": "environment", "score": 0.0006},
                            {"label": "labour", "score": 0.0006},
                            {"label": "sport", "score": 0.0006},
                            {"label": "education", "score": 0.0005},
                            {"label": "science and technology", "score": 0.0005},
                            {"label": "society", "score": 0.0005},
                            {
                                "label": "disaster, accident and emergency incident",
                                "score": 0.0002,
                            },
                            {"label": "lifestyle and leisure", "score": 0.0002},
                            {"label": "none", "score": 0.0002},
                            {"label": "religion", "score": 0.0001},
                            {"label": "weather", "score": 0.0001},
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
        "http://serve:8000/iptc-00000000/v1/predict",
        json=payload,
    )

    assert response.status_code == 200
    # TODO: assert score close to expected
    iptc = response.json()
    assert iptc == expected_response
