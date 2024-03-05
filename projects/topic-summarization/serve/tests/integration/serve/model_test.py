"""Prediction model tests."""
# isort: skip_file

# 3rd party libraries
import pytest

# Source
from src.settings import get_settings
from src.serve.category_storage import Category_list
from src.serve.schema import PredictRequestSchema
from src.serve.model import ServedTopicModel

settings = get_settings()


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


@pytest.mark.order(4)
def test_served_topic_model_predict(
    test_predict_input, test_inference_params, test_expected_predict_output
):
    """Tests the fully initialized and loaded ServedTopicModel's predict method."""
    served_topic_model = ServedTopicModel()
    served_topic_model.load()

    test_input = PredictRequestSchema.from_data(
        namespace=settings.model_name,
        parameters=test_inference_params,
        attributes={"content": test_predict_input},
    )

    test_actual_predict_output = served_topic_model.predict(test_input)

    assert set(test_actual_predict_output.attributes.topic.keys()).issubset(
        set(
            Category_list
            + [
                "Summary",
                "Theme",
            ]
        )
    )


@pytest.mark.order(3)
def test_served_topic_model_bio(test_expected_bio_output):
    """Tests the fully initialized and loaded ServedTopicModel's bio method."""
    served_topic_model = ServedTopicModel()

    served_topic_model.load()

    test_actual_bio_output = served_topic_model.bio()

    assert test_actual_bio_output == test_expected_bio_output
