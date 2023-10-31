"""Prediction model tests."""

# 3rd party libraries
import pytest

# Source
from src.serve.served_model import ServedLshModel


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
def test_served_lsh_model_predict(test_predict_input, test_expected_predict_output):
    """Tests the fully initialized and loaded ServedLshModel's predict method."""
    served_lsh_model = ServedLshModel()
    served_lsh_model.load()

    input_ = {
        "identifier": None,
        "namespace": "lsh",
        "attributes": {"content": test_predict_input},  # noqa
        "parameters": {
            "language": "en",
            "shingle_list": 5,
            "threshold": 0.6,
            "num_perm": 128,
        },
    }

    test_actual_predict_output = served_lsh_model.predict(input_)

    assert test_actual_predict_output == test_expected_predict_output


@pytest.mark.order(3)
def test_served_lsh_model_bio(test_expected_bio_output):
    """Tests the fully initialized and loaded ServedLshModel's bio method."""
    served_lsh_model = ServedLshModel()

    served_lsh_model.load()

    test_actual_bio_output = served_lsh_model.bio()

    assert test_actual_bio_output == test_expected_bio_output
