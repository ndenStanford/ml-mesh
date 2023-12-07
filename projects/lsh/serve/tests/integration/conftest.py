"""Conftest."""

# Standard Library
from typing import List

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
                    "AAAAAHoQC+YAAAAACA8jAgAAAAAVKX9QAAAAAHqyEgMAAAAAIhuY/wAAAAAUT4vZAAAAAErnGNA=",
                    "AAAAABQHCzsAAAAALnkFOQAAAAB4qFdzAAAAAJN9xeQAAAAACwovOwAAAABGdXidAAAAAA1Z+PI=",
                    "AAAAAD4U8b8AAAAAH7MdMAAAAAAVM+EpAAAAAAQD/58AAAAADW9d+gAAAAAcq6nYAAAAAFG8p54=",
                    "AAAAAExuWL0AAAAACjMnmwAAAABMfmzrAAAAAB+6ipsAAAAAGaQJJwAAAAAoMmz5AAAAAAFufIs=",
                    "AAAAABHLfvkAAAAADF2yVgAAAAA9Hy1BAAAAAADXBYAAAAAAnobt9QAAAAAT2EiPAAAAADL9q0M=",
                    "AAAAAAAcyQ0AAAAACp3nsAAAAAAypQctAAAAADtv3XoAAAAAFjAQNgAAAAAm2QFtAAAAAH1nNj0=",
                    "AAAAADd8PnEAAAAABZGJCgAAAABFIs7IAAAAAAnpSPwAAAAAPFgG8AAAAAARY8e1AAAAAFo3LWE=",
                    "AAAAAEZlAmMAAAAAEkQERgAAAAAG+hByAAAAADBIF9QAAAAAF2Vv1AAAAAAOwibZAAAAABypSaU=",
                    "AAAAAJfi2FUAAAAAMlrf6wAAAAAMsvwMAAAAAAcqgDkAAAAAJt3WcgAAAACI+lvdAAAAAADAYNM=",
                    "AAAAABj/2b8AAAAAB/ZJtwAAAAAV3og9AAAAAE3EegYAAAAADnxtIwAAAAAsIBceAAAAABhcX2I=",
                    "AAAAAGzSo4sAAAAAOX7WqQAAAAAFLB78AAAAADfKYS4AAAAAmKXv2AAAAABoagY4AAAAAAawUeI=",
                    "AAAAACYAZH4AAAAAKWWFjAAAAAAfeuLCAAAAAAw1MuQAAAAAPtvZ/wAAAAApA6d9AAAAAAIVqRk=",
                    "AAAAAA8Da5kAAAAAHUSP+wAAAAAB+0C/AAAAAAZLcIAAAAAAJdPABAAAAAAt5f9lAAAAAD3STkw=",
                    "AAAAABMLNHkAAAAApdiHbwAAAAATFmFDAAAAABtsENQAAAAAMSLylAAAAAA0H19/AAAAAE3GNWw=",
                    "AAAAACU1hbEAAAAABtQnTAAAAABhTbG3AAAAADcOlOQAAAAADGXo8gAAAAACFAy3AAAAAHsSvxM=",
                    "AAAAAATiCq4AAAAAMuDmuAAAAAATUap3AAAAACXCm6UAAAAAKH6CRAAAAAAXIBe3AAAAAAV2ywE=",
                    "AAAAACIAmGMAAAAAcSAguQAAAABG7iWIAAAAABw2lrsAAAAAMqL46QAAAAAVRTMWAAAAABqJ3jM=",
                    "AAAAACLs1yMAAAAACeLl7AAAAAB84gjfAAAAAENRjaAAAAAAFvruLAAAAAAgOb/1AAAAAA1Evss=",
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
        attributes={"model_name": "lsh"},
    )
