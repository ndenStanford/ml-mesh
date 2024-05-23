"""Prediction model tests."""

# Standard Library
from unittest.mock import patch

# 3rd party libraries
import pytest

# Source
from src.serve.schemas import PredictRequestSchema, PredictResponseSchema
from src.serve.served_model import ServedIPTCMultiModel
from src.settings import get_settings


settings = get_settings()


@pytest.mark.order(1)
def test_served_iptc_multi_model__init__():
    """Tests the constructor of the ServedIPTCMultiModel."""
    ServedIPTCMultiModel()


@pytest.mark.order(2)
def test_served_iptc_multi_model_load():
    """Tests the constructor of the ServedIPTCMultiModel."""
    served_iptc_multi_model = ServedIPTCMultiModel()
    assert not served_iptc_multi_model.is_ready()

    served_iptc_multi_model.load()

    assert served_iptc_multi_model.is_ready()


@pytest.mark.order(3)
@pytest.mark.parametrize(
    "payload, mock_return_values, expected_response",
    [
        (
            {
                "data": {
                    "identifier": None,
                    "namespace": "iptc-multi",
                    "attributes": {"content": "advanced science content"},
                    "parameters": {},
                }
            },
            {
                "combined": {},
                "processed": {},
                "postprocessed": [
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
                ],
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
@patch("src.serve.served_model.ServedIPTCMultiModel._postprocess_predictions")
@patch("src.serve.served_model.ServedIPTCMultiModel._process_combined_predictions")
@patch("src.serve.served_model.ServedIPTCMultiModel._get_combined_prediction")
def test_predict(
    mock_get_combined_prediction,
    mock_process_combined_predictions,
    mock_postprocess_predictions,
    payload,
    mock_return_values,
    expected_response,
):
    """Test the predict method processes inputs correctly."""
    model = ServedIPTCMultiModel()
    model.load()  # Sets the model to ready
    request_schema = PredictRequestSchema(**payload)

    mock_get_combined_prediction.return_value = mock_return_values["combined"]
    mock_process_combined_predictions.return_value = mock_return_values["processed"]
    mock_postprocess_predictions.return_value = mock_return_values["postprocessed"]

    response = model.predict(request_schema)

    assert isinstance(
        response, PredictResponseSchema
    ), "The response should be an instance of PredictResponseSchema"
    response_data = [
        {"label": t.label, "score": t.score, "mediatopic_id": t.mediatopic_id}
        for t in response.data.attributes.iptc_topic
    ]
    assert (
        response_data == expected_response["data"]["attributes"]["iptc_topic"]
    ), "The response data does not match the expected results"


@pytest.mark.order(3)
def test_served_iptc_multi_model_bio(test_expected_bio_output):
    """Tests the fully initialized and loaded ServedIPTCMultiModel's bio method."""
    served_iptc_multi_model = ServedIPTCMultiModel()

    served_iptc_multi_model.load()

    test_actual_bio_output = served_iptc_multi_model.bio()

    assert test_actual_bio_output == test_expected_bio_output
