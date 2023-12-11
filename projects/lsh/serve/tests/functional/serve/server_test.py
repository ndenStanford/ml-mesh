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
    assert readiness_response.json()["data"]["attributes"].get("model_name") is not None


@pytest.mark.parametrize(
    "payload, expected_response",
    [
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
                            "AAAAAHoQC+YAAAAACA8jAgAAAAAVKX9QAAAAAHqyEgMAAAAAIhuY/wAAAAAUT4vZAAAAAErnGNA=",  # noqa
                            "AAAAABQHCzsAAAAALnkFOQAAAAB4qFdzAAAAAJN9xeQAAAAACwovOwAAAABGdXidAAAAAA1Z+PI=",  # noqa
                            "AAAAAD4U8b8AAAAAH7MdMAAAAAAVM+EpAAAAAAQD/58AAAAADW9d+gAAAAAcq6nYAAAAAFG8p54=",  # noqa
                            "AAAAAExuWL0AAAAACjMnmwAAAABMfmzrAAAAAB+6ipsAAAAAGaQJJwAAAAAoMmz5AAAAAAFufIs=",  # noqa
                            "AAAAABHLfvkAAAAADF2yVgAAAAA9Hy1BAAAAAADXBYAAAAAAnobt9QAAAAAT2EiPAAAAADL9q0M=",  # noqa
                            "AAAAAAAcyQ0AAAAACp3nsAAAAAAypQctAAAAADtv3XoAAAAAFjAQNgAAAAAm2QFtAAAAAH1nNj0=",  # noqa
                            "AAAAADd8PnEAAAAABZGJCgAAAABFIs7IAAAAAAnpSPwAAAAAPFgG8AAAAAARY8e1AAAAAFo3LWE=",  # noqa
                            "AAAAAEZlAmMAAAAAEkQERgAAAAAG+hByAAAAADBIF9QAAAAAF2Vv1AAAAAAOwibZAAAAABypSaU=",  # noqa
                            "AAAAAJfi2FUAAAAAMlrf6wAAAAAMsvwMAAAAAAcqgDkAAAAAJt3WcgAAAACI+lvdAAAAAADAYNM=",  # noqa
                            "AAAAABj/2b8AAAAAB/ZJtwAAAAAV3og9AAAAAE3EegYAAAAADnxtIwAAAAAsIBceAAAAABhcX2I=",  # noqa
                            "AAAAAGzSo4sAAAAAOX7WqQAAAAAFLB78AAAAADfKYS4AAAAAmKXv2AAAAABoagY4AAAAAAawUeI=",  # noqa
                            "AAAAACYAZH4AAAAAKWWFjAAAAAAfeuLCAAAAAAw1MuQAAAAAPtvZ/wAAAAApA6d9AAAAAAIVqRk=",  # noqa
                            "AAAAAA8Da5kAAAAAHUSP+wAAAAAB+0C/AAAAAAZLcIAAAAAAJdPABAAAAAAt5f9lAAAAAD3STkw=",  # noqa
                            "AAAAABMLNHkAAAAApdiHbwAAAAATFmFDAAAAABtsENQAAAAAMSLylAAAAAA0H19/AAAAAE3GNWw=",  # noqa
                            "AAAAACU1hbEAAAAABtQnTAAAAABhTbG3AAAAADcOlOQAAAAADGXo8gAAAAACFAy3AAAAAHsSvxM=",  # noqa
                            "AAAAAATiCq4AAAAAMuDmuAAAAAATUap3AAAAACXCm6UAAAAAKH6CRAAAAAAXIBe3AAAAAAV2ywE=",  # noqa
                            "AAAAACIAmGMAAAAAcSAguQAAAABG7iWIAAAAABw2lrsAAAAAMqL46QAAAAAVRTMWAAAAABqJ3jM=",  # noqa
                            "AAAAACLs1yMAAAAACeLl7AAAAAB84gjfAAAAAENRjaAAAAAAFvruLAAAAAAgOb/1AAAAAA1Evss=",  # noqa
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
        "http://serve:8000/lsh/v1/predict",
        json=payload,
    )

    assert response.status_code == 200
    # TODO: assert score close to expected
    assert response.json() == expected_response
