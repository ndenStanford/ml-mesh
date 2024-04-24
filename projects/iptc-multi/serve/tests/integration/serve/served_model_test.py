"""Prediction model tests."""

# 3rd party libraries
import pytest

# Source
from src.serve.schemas import PredictRequestSchema
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
def test_served_iptc_multi_model_predict(
    test_predict_input, test_inference_params, test_expected_predict_output
):
    """Tests the fully initialized and loaded ServedIPTCMultiModel's predict method."""
    served_iptc_multi_model = ServedIPTCMultiModel()
    served_iptc_multi_model.load()

    test_input = PredictRequestSchema.from_data(
        namespace=settings.model_name,
        parameters=test_inference_params,
        attributes={"content": test_predict_input},
    )

    test_actual_predict_output = served_iptc_multi_model.predict(test_input)

    assert test_actual_predict_output == test_expected_predict_output


@pytest.mark.order(3)
def test_served_iptc_multi_model_bio(test_expected_bio_output):
    """Tests the fully initialized and loaded ServedIPTCMultiModel's bio method."""
    served_iptc_multi_model = ServedIPTCMultiModel()

    served_iptc_multi_model.load()

    test_actual_bio_output = served_iptc_multi_model.bio()

    assert test_actual_bio_output == test_expected_bio_output
