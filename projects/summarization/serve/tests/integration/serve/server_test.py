"""Model test."""


def test_get_model_server(test_client):
    """Integration test for the get_model_server function."""
    response = test_client.get("/summarization/v1/")

    assert response.status_code == 200
