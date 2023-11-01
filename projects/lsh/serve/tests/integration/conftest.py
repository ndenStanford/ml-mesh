"""Conftest."""

# Standard Library
from typing import Dict, List

# 3rd party libraries
import pytest
from fastapi.testclient import TestClient

# Internal libraries
from onclusiveml.serving.rest.serve import ServingParams

# Source
from src.serve.model_server import model_server
from src.serve.schemas import BioResponseSchema


@pytest.fixture
def test_serving_params():
    """Serving params fixture."""
    return ServingParams()


@pytest.fixture
def test_client():
    """Client fixture."""
    return TestClient(model_server)


@pytest.fixture
def test_predict_input() -> str:
    """Predict input fixture."""
    return "Call functions to generate hash signatures for each article"


@pytest.fixture
def test_inference_params() -> str:
    """Predict input fixture."""
    return {"language": "en", "shingle_list": 5, "threshold": 0.6, "num_perm": 128}


@pytest.fixture
def test_expected_predict_output() -> List[str]:
    """Expected predict output fixture."""
    return {
        "version": 1,
        "data": {
            "identifier": None,
            "namespace": "lsh",
            "attributes": {
                "signature": [
                    "AAAAAD7VrJYAAAAAUtj2YwAAAABnUo5LAAAAAKEQ6osAAAAAGN7zAQAAAACvI05uAAAAAP5T14M=",
                    "AAAAAImeBE8AAAAArLzBiwAAAABXJtUuAAAAADuLk0EAAAAABdQyawAAAABsuvhdAAAAAA1DABQ=",
                    "AAAAAN80jQ0AAAAA4AMsTwAAAAAdQ+nJAAAAADQX7AwAAAAAOInWSgAAAADW8ezsAAAAALmkSmc=",
                    "AAAAAEdhYYkAAAAAdlWvggAAAABKailoAAAAAAIxAgoAAAAATpd/swAAAABwtMk4AAAAABkBF2c=",
                    "AAAAAMTyc2oAAAAARNwyWAAAAABz/P6bAAAAACTaVUQAAAAAMoyr9gAAAACESd6KAAAAAFgDYYc=",
                    "AAAAAFKn1w8AAAAA3LGTrAAAAAAJJ73aAAAAAAtnQgYAAAAAc4I7eAAAAAD08z7vAAAAAEWmb0M=",
                    "AAAAANYBf2oAAAAAU59svQAAAABWfyecAAAAAO+fMSoAAAAA/AEiWQAAAADi76dRAAAAACZAFWI=",
                    "AAAAAKceSGYAAAAAHHnbRwAAAACNhF50AAAAAHgsIHIAAAAALQe0tgAAAACl0hKtAAAAANjd5Gw=",
                    "AAAAAJFzk3gAAAAAMxIZewAAAABmmIwNAAAAANKJgxMAAAAAaeBdxQAAAAByhAtTAAAAAKoPEtA=",
                    "AAAAAD//H6QAAAAAR2MGtQAAAADuHvbsAAAAANOxgcsAAAAAbMURIgAAAABUGFjvAAAAAA2+Lew=",
                    "AAAAADJ0nxwAAAAAEDygXwAAAAC5rKeMAAAAAMHGBJAAAAAAVbu+HAAAAACvnHsdAAAAAPZ4r3I=",
                    "AAAAAIsaapQAAAAA4UNh0wAAAAD29SlWAAAAAKgaBv4AAAAABK518AAAAACE0OvYAAAAAPYUu7c=",
                    "AAAAAPgAVJoAAAAAR8Y3RQAAAAD1tPyTAAAAAPeLD0EAAAAAnAxBywAAAABKiF6rAAAAAGoBEXA=",
                    "AAAAAGQyfFMAAAAAGFRsIAAAAAAiQRcGAAAAADzs6CYAAAAABT6eXgAAAADBDsR/AAAAAKjSFEc=",
                    "AAAAAMsg8FIAAAAAFm7yPAAAAAA5Au8cAAAAAGYhiuUAAAAA9jbZdQAAAAB2X3QvAAAAAO+93YE=",
                    "AAAAAOrGfusAAAAA4UQsGgAAAAB9n0NhAAAAAFDZRUIAAAAAbKUEUQAAAABSgqcrAAAAANReZwE=",
                    "AAAAANrB0GcAAAAAkNMRaAAAAAA0QhyKAAAAABLE06gAAAAAzi1LqAAAAACo+jipAAAAAIUoHM4=",
                    "AAAAAHxFrisAAAAAkf5FlgAAAACQ7ru+AAAAAO4TeqUAAAAAcsOYLwAAAAAHk+gFAAAAAHSHwzQ=",
                ]
            },
        },
    }


@pytest.fixture
def test_expected_bio_output():
    """Test expected bio output."""
    return BioResponseSchema.from_data(
        version=1,
        namespace="lsh",
        attributes={"model_name": "lsh", "model_card": Dict},
    )
