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
    root_response = requests.get("http://serve:8000/iptc-multi/v1/")

    assert root_response.status_code == 200


def test_model_server_liveness():
    """Tests the liveness endpoint of a ModelServer (not running) instance."""
    liveness_response = requests.get("http://serve:8000/iptc-multi/v1/live")

    assert liveness_response.status_code == 200
    assert liveness_response.json() == LivenessProbeResponse().dict()


def test_model_server_readiness():
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    readiness_response = requests.get("http://serve:8000/iptc-multi/v1/ready")

    assert readiness_response.status_code == 200
    assert readiness_response.json() == ReadinessProbeResponse().dict()


def test_model_server_bio():
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    readiness_response = requests.get("http://serve:8000/iptc-multi/v1/bio")

    assert readiness_response.status_code == 200
    assert readiness_response.json()["data"]["attributes"].get("model_name") is not None


@pytest.mark.parametrize(
    "payload, expected_response",
    [
        (
            {
                "data": {
                    "namespace": "iptc-multi",
                    "attributes": {"content": "mathemetics"},  # noqa
                    "parameters": {"language": "en"},
                }
            },
            {
                "version": 1,
                "data": {
                    "identifier": None,
                    "namespace": "iptc-multi",
                    "attributes": {
                        "iptc_topic": [
                            {
                                "label": "science and technology",
                                "score": 0.994,
                                "mediatopic_id": "13000000",
                            },
                            {
                                "label": "science and technology > natural science",
                                "score": 0.993,
                                "mediatopic_id": "20000717",
                            },
                            {
                                "label": "science and technology > natural science > biology",
                                "score": 0.47,
                                "mediatopic_id": "20000719",
                            },
                            {
                                "label": "science and technology > natural science > astronomy",
                                "score": 0.186,
                                "mediatopic_id": "20000718",
                            },
                            {
                                "label": "science and technology > natural science > physics",
                                "score": 0.114,
                                "mediatopic_id": "20000731",
                            },
                        ]
                    },
                },
            },
        )
    ],
)
def test_model_server_prediction(payload, expected_response):
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    response = requests.post(
        "http://serve:8000/iptc-multi/v1/predict",
        json=payload,
    )

    assert response.status_code == 200
    # TODO: assert score close to expected
    assert response.json() == expected_response
