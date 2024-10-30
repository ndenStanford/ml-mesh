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
    liveness_response = requests.get("http://serve:8000/iptc-multi/v1/live")

    assert liveness_response.status_code == 200
    assert liveness_response.json() == LivenessProbeResponse().model_dump()


def test_model_server_readiness():
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    readiness_response = requests.get("http://serve:8000/iptc-multi/v1/ready")

    assert readiness_response.status_code == 200
    assert readiness_response.json() == ReadinessProbeResponse().model_dump()


def test_model_server_bio():
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    readiness_response = requests.get("http://serve:8000/iptc-multi/v1/bio")

    assert readiness_response.status_code == 200
    assert readiness_response.json()["data"]["attributes"].get("model_name") is not None


@pytest.mark.parametrize(
    "payload, status_code,expected_response",
    [
        (
            {
                "data": {
                    "namespace": "iptc-multi",
                    "attributes": {
                        "content": "Ten-year US yields approached 4.5%. The S&P 500 fluctuated, with the benchmark headed toward its fourth straight week of gains. Stocks will finish trading at 1 p.m. New York time in observance of Thanksgiving, and the recommended close for the Treasury cash"
                    },  # noqa
                    "parameters": {"language": "en"},
                }
            },
            200,
            {
                "data": {
                    "attributes": {
                        "iptc_topic": [
                            {
                                "label": "economy, business and finance",
                                "mediatopic_id": "04000000",
                                "score": 0.994,
                            },
                            {
                                "label": "economy, business and finance > market and exchange",
                                "mediatopic_id": "20000385",
                                "score": 0.971,
                            },
                            {
                                "label": "economy, business and finance > market and exchange > business governance",
                                "mediatopic_id": "20000199",
                                "score": 0.85,
                            },
                        ]
                    },
                    "identifier": None,
                    "namespace": "iptc-multi",
                },
                "version": 1,
            },
        )
    ],
)
def test_model_server_prediction(payload, status_code, expected_response):
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    response = requests.post(
        "http://serve:8000/iptc-multi/v1/predict",
        json=payload,
    )

    assert response.status_code == status_code
    assert response.json() == expected_response


@pytest.mark.parametrize(
    "payload, status_code",
    [
        (
            {
                "data": {
                    "namespace": "iptc-multi",
                    "attributes": {"content": "crime"},  # noqa
                    "parameters": {"language": "xyz"},
                }
            },
            204,
        )
    ],
)
def test_model_server_prediction_unsupported_language(payload, status_code):
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    response = requests.post(
        "http://serve:8000/iptc-multi/v1/predict",
        json=payload,
    )

    assert response.status_code == status_code
