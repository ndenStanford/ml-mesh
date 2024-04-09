"""Server functional tests."""

# 3rd party libraries
import requests

# Internal libraries
from onclusiveml.serving.rest.serve import (
    LivenessProbeResponse,
    ReadinessProbeResponse,
)


def test_server_root():
    """Tests the root endpoint of a ModelServer (not running) instance."""
    root_response = requests.get("http://serve:8888/transcript-segmentation/v1/")

    assert root_response.status_code == 200


def test_server_liveness():
    """Tests the liveness endpoint of a ModelServer (not running) instance."""
    liveness_response = requests.get(
        "http://serve:8888/transcript-segmentation/v1/live"
    )

    assert liveness_response.status_code == 200
    assert liveness_response.json() == LivenessProbeResponse().dict()


def test_server_readiness():
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    readiness_response = requests.get(
        "http://serve:8888/transcript-segmentation/v1/ready"
    )

    assert readiness_response.status_code == 200
    assert readiness_response.json() == ReadinessProbeResponse().dict()


def test_server_bio():
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    readiness_response = requests.get(
        "http://serve:8888/transcript-segmentation/v1/bio"
    )

    assert readiness_response.status_code == 200
    assert readiness_response.json()["data"]["attributes"].get("model_name") is not None


def test_server_prediction(test_payload, expected_response):
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    response = requests.post(
        "http://serve:8888/transcript-segmentation/v1/predict",
        json=test_payload,
    )

    assert response.status_code == 200
    assert response.json()["version"] == expected_response["version"]
    assert (
        response.json()["data"]["identifier"] == expected_response["data"]["identifier"]
    )
    assert (
        response.json()["data"]["namespace"] == expected_response["data"]["namespace"]
    )
    assert (
        abs(
            response.json()["data"]["attributes"]["start_time"]
            - expected_response["data"]["attributes"]["start_time"]
        )
        <= 20000
    )
    assert (
        abs(
            response.json()["data"]["attributes"]["end_time"]
            - expected_response["data"]["attributes"]["end_time"]
        )
        <= 20000
    )
    assert (
        abs(
            response.json()["data"]["attributes"]["transcript_start_time"]
            - expected_response["data"]["attributes"]["transcript_start_time"]
        )
        <= 20000
    )
    assert (
        abs(
            response.json()["data"]["attributes"]["transcript_end_time"]
            - expected_response["data"]["attributes"]["transcript_end_time"]
        )
        <= 20000
    )
    assert isinstance(response.json()["data"]["attributes"]["title"], str)
    assert isinstance(response.json()["data"]["attributes"]["summary"], str)
    assert isinstance(response.json()["data"]["attributes"]["segment"], str)
    assert (
        response.json()["data"]["attributes"]["ad"]
        == expected_response["data"]["attributes"]["ad"]
    )


def test_server_prediction_o2(test_payload_o2, expected_response_o2):
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    response = requests.post(
        "http://serve:8888/transcript-segmentation/v1/predict",
        json=test_payload_o2,
    )

    assert response.status_code == 200
    assert response.json()["version"] == expected_response_o2["version"]
    assert (
        response.json()["data"]["identifier"]
        == expected_response_o2["data"]["identifier"]
    )
    assert (
        response.json()["data"]["namespace"]
        == expected_response_o2["data"]["namespace"]
    )
    assert (
        abs(
            response.json()["data"]["attributes"]["start_time"]
            - expected_response_o2["data"]["attributes"]["start_time"]
        )
        <= 0
    )
    assert (
        abs(
            response.json()["data"]["attributes"]["end_time"]
            - expected_response_o2["data"]["attributes"]["end_time"]
        )
        <= 0
    )
    assert (
        abs(
            response.json()["data"]["attributes"]["transcript_start_time"]
            - expected_response_o2["data"]["attributes"]["transcript_start_time"]
        )
        <= 0
    )
    assert (
        abs(
            response.json()["data"]["attributes"]["transcript_end_time"]
            - expected_response_o2["data"]["attributes"]["transcript_end_time"]
        )
        <= 0
    )
    assert isinstance(response.json()["data"]["attributes"]["title"], str)
    assert isinstance(response.json()["data"]["attributes"]["summary"], str)
    assert isinstance(response.json()["data"]["attributes"]["segment"], str)
    assert (
        response.json()["data"]["attributes"]["ad"]
        == expected_response_o2["data"]["attributes"]["ad"]
    )


def test_server_prediction_timeout(test_payload_timeout, expected_response_timeout):
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    response = requests.post(
        "http://serve:8888/transcript-segmentation/v1/predict",
        json=test_payload_timeout,
    )
    print(response.json())

    assert response.status_code == 200
    assert response.json()["version"] == expected_response_timeout["version"]
    assert (
        response.json()["data"]["identifier"]
        == expected_response_timeout["data"]["identifier"]
    )
    assert (
        response.json()["data"]["namespace"]
        == expected_response_timeout["data"]["namespace"]
    )
    assert (
        abs(
            response.json()["data"]["attributes"]["start_time"]
            - expected_response_timeout["data"]["attributes"]["start_time"]
        )
        <= 20000
    )
    assert (
        abs(
            response.json()["data"]["attributes"]["end_time"]
            - expected_response_timeout["data"]["attributes"]["end_time"]
        )
        <= 20000
    )
    assert (
        abs(
            response.json()["data"]["attributes"]["transcript_start_time"]
            - expected_response_timeout["data"]["attributes"]["transcript_start_time"]
        )
        <= 20000
    )
    assert (
        abs(
            response.json()["data"]["attributes"]["transcript_end_time"]
            - expected_response_timeout["data"]["attributes"]["transcript_end_time"]
        )
        <= 20000
    )
    assert isinstance(response.json()["data"]["attributes"]["title"], str)
    assert isinstance(response.json()["data"]["attributes"]["summary"], str)
    assert isinstance(response.json()["data"]["attributes"]["segment"], str)
    assert (
        response.json()["data"]["attributes"]["ad"]
        == expected_response_timeout["data"]["attributes"]["ad"]
    )
