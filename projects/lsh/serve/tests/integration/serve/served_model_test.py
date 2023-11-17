"""Prediction model tests."""

# 3rd party libraries
import pytest

# Source
from src.serve.schemas import PredictRequestSchema
from src.serve.served_model import ServedLshModel
from src.settings import get_settings


settings = get_settings()


@pytest.mark.order(1)
def test_served_lsh_model__init__():
    """Tests the constructor of the ServedLshModel."""
    ServedLshModel()


@pytest.mark.order(2)
def test_served_lsh_model_load():
    """Tests the constructor of the ServedLSHModel."""
    served_lsh_model = ServedLshModel()
    assert not served_lsh_model.is_ready()

    served_lsh_model.load()

    assert served_lsh_model.is_ready()


@pytest.mark.order(3)
def test_served_lsh_model_predict(
    test_predict_input, test_inference_params, test_expected_predict_output
):
    """Tests the fully initialized and loaded ServedLshModel's predict method."""
    served_lsh_model = ServedLshModel()
    served_lsh_model.load()

    test_input = PredictRequestSchema.from_data(
        namespace=settings.model_name,
        parameters=test_inference_params,
        attributes={"content": test_predict_input},
    )

    test_actual_predict_output = served_lsh_model.predict(test_input)

    assert test_actual_predict_output == test_expected_predict_output


@pytest.mark.order(3)
def test_served_lsh_model_bio(test_expected_bio_output):
    """Tests the fully initialized and loaded ServedLshModel's bio method."""
    served_lsh_model = ServedLshModel()

    served_lsh_model.load()

    test_actual_bio_output = served_lsh_model.bio()

    assert test_actual_bio_output == test_expected_bio_output
