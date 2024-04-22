"""Model server."""
# isort: skip_file

# 3rd party libraries
import pytest

# Internal libraries

# Source
from src.settings import get_settings

settings = get_settings()


@pytest.mark.order(7)
def test_model_server_predict_sample_docs(
    test_client, test_model_name, test_payload_sample_docs
):
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    test_response = test_client.post(
        f"/{test_model_name}/v1/predict", json=test_payload_sample_docs
    )
    assert test_response.status_code == 200
    assert test_response.json()["data"]["attributes"]["topic"] is not None
