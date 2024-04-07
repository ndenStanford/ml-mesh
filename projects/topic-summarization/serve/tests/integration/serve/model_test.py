"""Prediction model tests."""
# isort: skip_file

# 3rd party libraries
import pytest
from freezegun import freeze_time

# Source
from src.settings import get_settings
from src.serve.category_storage import Category_list
from src.serve.schema import PredictRequestSchema
from src.serve.model import ServedTopicModel
from onclusiveml.serving.serialization.topic_summarization.v1 import ImpactCategoryLabel

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


@freeze_time("2024-03-15 15:01:00", tick=True)
@pytest.mark.order(4)
def test_served_topic_model_predict(test_inference_params):
    """Tests the ServedTopicModel's predict method."""
    served_topic_model = ServedTopicModel()
    served_topic_model.load()

    test_input = PredictRequestSchema.from_data(
        namespace=settings.model_name,
        parameters=test_inference_params,
        attributes={
            "profile_id": """("Apple Music" OR AppleMusic) AND sourcecountry:[ESP,AND] AND sourcetype:print""",  # noqa: E501
            "topic_id": 257,
            "trend_detection": True,
        },
    )
    test_actual_predict_output = served_topic_model.predict(test_input)
    print("%" * 20)
    print(test_actual_predict_output)
    assert set(test_actual_predict_output.attributes.topic.keys()).issubset(
        set(
            Category_list
            + [
                "Summary",
                "Theme",
            ]
        )
    )

    assert (
        test_actual_predict_output.attributes.impact_category == ImpactCategoryLabel.low
    )


@freeze_time("2024-03-15 15:01:00", tick=True)
@pytest.mark.order(6)
def test_served_topic_model_predict_skip_trend(test_inference_params):
    """Tests the ServedTopicModel's predict method without trend detection."""
    served_topic_model = ServedTopicModel()
    served_topic_model.load()

    test_input = PredictRequestSchema.from_data(
        namespace=settings.model_name,
        parameters=test_inference_params,
        attributes={
            "profile_id": """("Apple Music" OR AppleMusic) AND sourcecountry:[ESP,AND] AND sourcetype:print""",  # noqa: E501
            "topic_id": 257,
            "trend_detection": False,
        },
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

    assert (
        test_actual_predict_output.attributes.impact_category == ImpactCategoryLabel.low
    )


@pytest.mark.order(3)
def test_served_topic_model_bio(test_expected_bio_output):
    """Tests the fully initialized and loaded ServedTopicModel's bio method."""
    served_topic_model = ServedTopicModel()

    served_topic_model.load()

    test_actual_bio_output = served_topic_model.bio()

    assert test_actual_bio_output == test_expected_bio_output
