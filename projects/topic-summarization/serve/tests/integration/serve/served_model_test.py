"""Prediction model tests."""

# 3rd party libraries
import pytest

# Source
from src.serve.category_storage import Category_list
from src.serve.served_model import ServedTopicModel
from src.serve.server_models import PredictRequestModel


@pytest.mark.order(1)
def test_served_topic_model__init__():
    """Tests the constructor of the ServedTopicModel."""
    ServedTopicModel()


@pytest.mark.order(2)
def test_served_topic_model_load():
    """Tests the constructor of the ServedTopicModel."""
    served_topic_model = ServedTopicModel()
    assert not served_topic_model.is_ready()

    served_topic_model.load()

    assert served_topic_model.is_ready()


@pytest.mark.order(3)
def test_served_topic_model_predict(test_predict_input, test_expected_predict_output):
    """Tests the fully initialized and loaded ServedTopicModel's predict method."""
    served_topic_model = ServedTopicModel()
    served_topic_model.load()

    input = PredictRequestModel(
        inputs=test_predict_input,
    )

    test_actual_predict_output = served_topic_model.predict(input)

    assert list(test_actual_predict_output.topic.keys()) == Category_list + [
        "Summary",
        "Theme",
    ]


@pytest.mark.order(3)
def test_served_topic_model_bio(test_expected_bio_output):
    """Tests the fully initialized and loaded ServedTopicModel's bio method."""
    served_topic_model = ServedTopicModel()

    served_topic_model.load()

    test_actual_bio_output = served_topic_model.bio()

    assert test_actual_bio_output == test_expected_bio_output
