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
    root_response = requests.get("http://serve:8000/lsh/v1/")

    assert root_response.status_code == 200


def test_model_server_liveness():
    """Tests the liveness endpoint of a ModelServer (not running) instance."""
    liveness_response = requests.get("http://serve:8000/lsh/v1/live")

    assert liveness_response.status_code == 200
    assert liveness_response.json() == LivenessProbeResponse().dict()


def test_model_server_readiness():
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    readiness_response = requests.get("http://serve:8000/lsh/v1/ready")

    assert readiness_response.status_code == 200
    assert readiness_response.json() == ReadinessProbeResponse().dict()


def test_model_server_bio():
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    readiness_response = requests.get("http://serve:8000/lsh/v1/bio")

    assert readiness_response.status_code == 200
    assert readiness_response.json()["data"]["attributes"].get("model_card") is not None


@pytest.mark.parametrize(
    "payload, expected_response",
    (
        {
            "data": {
                "namespace": "lsh",
                "attributes": {
                    "content": "Call functions to generate hash signatures for each article"  # noqa
                },
                "parameters": {
                    "language": "en",
                    "shingle_list": 5,
                    "threshold": 0.6,
                    "num_perm": 128,
                },
            }
        },
        {
            "version": 1,
            "data": {
                "identifier": None,
                "namespace": "lsh",
                "attributes": {
                    "signature": [
                        "AAAAAD7VrJYAAAAAUtj2YwAAAABnUo5LAAAAAKEQ6osAAAAAGN7zAQAAAACvI05uAAAAAP5T14M=",  # noqa
                        "AAAAAImeBE8AAAAArLzBiwAAAABXJtUuAAAAADuLk0EAAAAABdQyawAAAABsuvhdAAAAAA1DABQ=",  # noqa
                        "AAAAAN80jQ0AAAAA4AMsTwAAAAAdQ+nJAAAAADQX7AwAAAAAOInWSgAAAADW8ezsAAAAALmkSmc=",  # noqa
                        "AAAAAEdhYYkAAAAAdlWvggAAAABKailoAAAAAAIxAgoAAAAATpd/swAAAABwtMk4AAAAABkBF2c=",  # noqa
                        "AAAAAMTyc2oAAAAARNwyWAAAAABz/P6bAAAAACTaVUQAAAAAMoyr9gAAAACESd6KAAAAAFgDYYc=",  # noqa
                        "AAAAAFKn1w8AAAAA3LGTrAAAAAAJJ73aAAAAAAtnQgYAAAAAc4I7eAAAAAD08z7vAAAAAEWmb0M=",  # noqa
                        "AAAAANYBf2oAAAAAU59svQAAAABWfyecAAAAAO+fMSoAAAAA/AEiWQAAAADi76dRAAAAACZAFWI=",  # noqa
                        "AAAAAKceSGYAAAAAHHnbRwAAAACNhF50AAAAAHgsIHIAAAAALQe0tgAAAACl0hKtAAAAANjd5Gw=",  # noqa
                        "AAAAAJFzk3gAAAAAMxIZewAAAABmmIwNAAAAANKJgxMAAAAAaeBdxQAAAAByhAtTAAAAAKoPEtA=",  # noqa
                        "AAAAAD//H6QAAAAAR2MGtQAAAADuHvbsAAAAANOxgcsAAAAAbMURIgAAAABUGFjvAAAAAA2+Lew=",  # noqa
                        "AAAAADJ0nxwAAAAAEDygXwAAAAC5rKeMAAAAAMHGBJAAAAAAVbu+HAAAAACvnHsdAAAAAPZ4r3I=",  # noqa
                        "AAAAAIsaapQAAAAA4UNh0wAAAAD29SlWAAAAAKgaBv4AAAAABK518AAAAACE0OvYAAAAAPYUu7c=",  # noqa
                        "AAAAAPgAVJoAAAAAR8Y3RQAAAAD1tPyTAAAAAPeLD0EAAAAAnAxBywAAAABKiF6rAAAAAGoBEXA=",  # noqa
                        "AAAAAGQyfFMAAAAAGFRsIAAAAAAiQRcGAAAAADzs6CYAAAAABT6eXgAAAADBDsR/AAAAAKjSFEc=",  # noqa
                        "AAAAAMsg8FIAAAAAFm7yPAAAAAA5Au8cAAAAAGYhiuUAAAAA9jbZdQAAAAB2X3QvAAAAAO+93YE=",  # noqa
                        "AAAAAOrGfusAAAAA4UQsGgAAAAB9n0NhAAAAAFDZRUIAAAAAbKUEUQAAAABSgqcrAAAAANReZwE=",  # noqa
                        "AAAAANrB0GcAAAAAkNMRaAAAAAA0QhyKAAAAABLE06gAAAAAzi1LqAAAAACo+jipAAAAAIUoHM4=",  # noqa
                        "AAAAAHxFrisAAAAAkf5FlgAAAACQ7ru+AAAAAO4TeqUAAAAAcsOYLwAAAAAHk+gFAAAAAHSHwzQ=",  # noqa
                    ]
                },
            },
        },
    ),
)
def test_model_server_prediction(payload, expected_response):
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    response = requests.post(
        "http://serve:8000/lsh/v1/predict",
        json=payload,
    )

    assert response.status_code == 200
    # TODO: assert score close to expected
    assert response.json() == expected_response
