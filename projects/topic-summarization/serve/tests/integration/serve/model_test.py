"""Prediction model tests."""
# isort: skip_file

# 3rd party libraries
import pytest
from freezegun import freeze_time

# Source
from src.settings import get_settings
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
            "query_string": """("Apple Music" OR AppleMusic) AND sourcecountry:[ESP,AND] AND sourcetype:print""",  # noqa: E501
            "topic_id": 257,
            "trend_detection": True,
        },
    )
    test_actual_predict_output = served_topic_model.predict(test_input)
    assert test_actual_predict_output.attributes.topic is not None


@freeze_time("2024-03-15 15:01:00", tick=True)
@pytest.mark.order(4)
def test_served_topic_model_predict_query_id(test_inference_params):
    """Tests the ServedTopicModel's predict method."""
    served_topic_model = ServedTopicModel()
    served_topic_model.load()

    test_input = PredictRequestSchema.from_data(
        namespace=settings.model_name,
        parameters=test_inference_params,
        attributes={
            "query_id": "b529bdd8-47fd-4dbe-b105-53a02ced41cc",  # noqa: E501
            "topic_id": 257,
            "trend_detection": True,
        },
    )
    test_actual_predict_output = served_topic_model.predict(test_input)
    assert test_actual_predict_output.attributes.topic is not None


@freeze_time("2024-03-15 15:01:00", tick=True)
@pytest.mark.order(6)
def test_served_topic_model_predict_skip_trend(test_inference_params):
    """Tests ServedTopicModel's predict method without trend detection."""
    served_topic_model = ServedTopicModel()
    served_topic_model.load()

    test_input = PredictRequestSchema.from_data(
        namespace=settings.model_name,
        parameters=test_inference_params,
        attributes={
            "query_string": """((amex OR "american express" OR americanexpress) AND NOT ("nyse amex" OR "stade amex" OR abonnez-vous OR "American Express Global Business Travel" OR "american express gbt" OR "amex gbt" OR "amex global business travel" OR "William Muller" OR Sarrebourg )) OR "aXHH-Hotel hub" OR Euraxo OR aXcent OR "Carte Optima" OR "Carte SBS" OR "Carte Blue" OR Uvet OR Mobilextend OR Resoclub OR Resoclick OR Pcard OR "Nathalie Estrada" OR "Eric Tredjeu" OR "Sophie Janvier" OR "Cathy Notlet" OR "Claudine Hameau" OR "Stéphanie Laroque" OR "PF Brezes" OR "Hervé Sedky" OR "Gabrielle Elbaz" OR "Yves Pechon" OR  "Christophe Haviland" OR "Espace Voyages professionnels" OR Tripcase""",  # noqa: E501
            "topic_id": 19,
            "trend_detection": False,
        },
    )
    test_actual_predict_output = served_topic_model.predict(test_input)
    assert test_actual_predict_output.attributes.topic is not None


@pytest.mark.order(7)
def test_served_topic_model_predict_sample_content(
    test_predict_input, test_inference_params
):
    """Tests the fully ServedTopicModel's predict method with sample input."""
    served_topic_model = ServedTopicModel()
    served_topic_model.load()

    test_input = PredictRequestSchema.from_data(
        namespace=settings.model_name,
        parameters=test_inference_params,
        attributes={
            "content": test_predict_input,
        },
    )
    test_actual_predict_output = served_topic_model.predict(test_input)
    assert test_actual_predict_output.attributes.topic is not None

    assert test_actual_predict_output.attributes.impact_category is None


@pytest.mark.order(3)
def test_served_topic_model_bio(test_expected_bio_output):
    """Tests the fully initialized and loaded ServedTopicModel's bio method."""
    served_topic_model = ServedTopicModel()

    served_topic_model.load()

    test_actual_bio_output = served_topic_model.bio()

    assert test_actual_bio_output == test_expected_bio_output
