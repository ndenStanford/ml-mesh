"""Conftest."""

# Standard Library
import json
from typing import List

# 3rd party libraries
import pytest
from requests_toolbelt.sessions import BaseUrlSession

# Internal libraries
from onclusiveml.serving.rest.serve import ServingParams

# Source
from src.serve.server_models import BioResponseModel, PredictResponseModel


@pytest.fixture
def test_serving_params():
    """Serving params fixture."""
    return ServingParams()


@pytest.fixture
def test_client(test_serving_params):
    """Client-like session with base url to avoid duplication.

    References:
        https://toolbelt.readthedocs.io/en/latest/sessions.html#baseurlsession
    """
    test_model_server_url = f"http://serve:{test_serving_params.uvicorn_settings.port}"

    return BaseUrlSession(base_url=test_model_server_url)


@pytest.fixture
def test_model_name() -> str:
    """Model name fixture."""
    return "lsh"


@pytest.fixture
def test_inference_params(test_served_model_artifacts):
    """Test loading inference parameters."""
    with open(test_served_model_artifacts.inference_params_test_file, "r") as json_file:
        test_inference_params = json.load(json_file)

    return test_inference_params


@pytest.fixture
def test_predict_input() -> str:
    """Test predict input."""
    return "Call functions to generate hash signatures for each article"


@pytest.fixture
def test_expected_predict_output() -> List[str]:
    """Predicted response model fixture."""
    return PredictResponseModel(
        signature=[
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
    )


@pytest.fixture
def test_expected_bio_output(test_model_name):
    """Test bio output."""
    return BioResponseModel(model_name=test_model_name)
