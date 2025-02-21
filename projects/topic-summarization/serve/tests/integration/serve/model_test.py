"""Prediction model tests."""

# isort: skip_file
from unittest.mock import patch

# 3rd party libraries
import pandas as pd
import pytest
from datetime import datetime
from freezegun import freeze_time

# Source
from src.settings import get_settings
from src.serve.schema import PredictRequestSchema
from src.serve.model import ServedTopicModel
from src.serve.tables import TopicSummaryDynamoDB

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


@pytest.mark.order(3)
def test_served_topic_model_bio(test_expected_bio_output):
    """Tests the fully initialized and loaded ServedTopicModel's bio method."""
    served_topic_model = ServedTopicModel()

    served_topic_model.load()

    test_actual_bio_output = served_topic_model.bio()

    assert test_actual_bio_output == test_expected_bio_output


@freeze_time("2024-03-15 15:01:00", tick=True)
@pytest.mark.order(4)
def test_served_topic_model_predict(test_inference_params, test_new_es_index):
    """Tests the ServedTopicModel's predict method."""
    served_topic_model = ServedTopicModel()
    served_topic_model.load()
    with patch.object(
        served_topic_model.trend_detector, "es_index", new=test_new_es_index
    ), patch.object(
        served_topic_model.document_collector, "es_index", new=test_new_es_index
    ), patch.object(
        served_topic_model.impact_quantifier, "es_index", new=test_new_es_index
    ):
        # get_settings.cache_clear()

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
@patch.object(TopicSummaryDynamoDB, "save")
@pytest.mark.order(5)
def test_served_topic_model_predict_save_dynamodb(
    mock_topic_summary_dynamodb_save, test_inference_params, test_new_es_index
):
    """Tests the ServedTopicModel's predict method."""
    served_topic_model = ServedTopicModel()
    served_topic_model.load()

    with patch.object(
        served_topic_model.trend_detector, "es_index", new=test_new_es_index
    ), patch.object(
        served_topic_model.document_collector, "es_index", new=test_new_es_index
    ), patch.object(
        served_topic_model.impact_quantifier, "es_index", new=test_new_es_index
    ):

        test_input = PredictRequestSchema.from_data(
            namespace=settings.model_name,
            parameters=test_inference_params,
            attributes={
                "query_string": """("Apple Music" OR AppleMusic) AND sourcecountry:[ESP,AND] AND sourcetype:print""",  # noqa: E501
                "topic_id": 257,
                "trend_detection": True,
                "save_report_dynamodb": True,
            },
        )
        test_actual_predict_output = served_topic_model.predict(test_input)
        assert test_actual_predict_output.attributes.topic is not None

    mock_topic_summary_dynamodb_save.assert_called_once()


@freeze_time("2024-03-15 15:01:00", tick=True)
@pytest.mark.order(6)
def test_served_topic_model_predict_query_id(test_inference_params, test_new_es_index):
    """Tests the ServedTopicModel's predict method."""
    served_topic_model = ServedTopicModel()
    served_topic_model.load()

    with patch.object(
        served_topic_model.trend_detector, "es_index", new=test_new_es_index
    ), patch.object(
        served_topic_model.document_collector, "es_index", new=test_new_es_index
    ), patch.object(
        served_topic_model.impact_quantifier, "es_index", new=test_new_es_index
    ):

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


@freeze_time("2024-07-23 15:01:00", tick=True)
@pytest.mark.order(7)
def test_served_topic_model_predict_media_api_query(
    test_inference_params, test_media_api_es_index, test_media_api_query
):
    """Tests the ServedTopicModel's predict method."""
    served_topic_model = ServedTopicModel()
    served_topic_model.load()

    with patch.object(
        served_topic_model.trend_detector, "es_index", new=test_media_api_es_index
    ), patch.object(
        served_topic_model.document_collector, "es_index", new=test_media_api_es_index
    ), patch.object(
        served_topic_model.impact_quantifier, "es_index", new=test_media_api_es_index
    ):

        test_input = PredictRequestSchema.from_data(
            namespace=settings.model_name,
            parameters=test_inference_params,
            attributes={
                "media_api_query": test_media_api_query,  # noqa: E501
                "topic_id": 59,
                "trend_detection": True,
            },
        )
        inputs = test_input.attributes
        query_profile = served_topic_model.get_query_profile(inputs)
        topic_id = inputs.topic_id

        trend_end_time = pd.Timestamp(datetime.now())
        trend_start_time = trend_end_time - pd.Timedelta(days=14)
        topic_document_threshold = 0.01
        trend_time_interval = "12h"

        (
            trend_found,
            inflection_point,
            query_all_doc_count,
            query_topic_doc_count,
        ) = served_topic_model.trend_detector.single_topic_trend(
            query_profile,
            topic_id,
            trend_start_time,
            trend_end_time,
            topic_document_threshold,
            trend_time_interval,
        )
        assert query_all_doc_count is not None
        assert query_topic_doc_count is not None


@freeze_time("2024-03-15 15:01:00", tick=True)
@pytest.mark.order(7)
def test_served_topic_model_predict_skip_trend(
    test_inference_params, test_new_es_index
):
    """Tests ServedTopicModel's predict method without trend detection."""
    served_topic_model = ServedTopicModel()
    served_topic_model.load()
    with patch.object(
        served_topic_model.trend_detector, "es_index", new=test_new_es_index
    ), patch.object(
        served_topic_model.document_collector, "es_index", new=test_new_es_index
    ), patch.object(
        served_topic_model.impact_quantifier, "es_index", new=test_new_es_index
    ):

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


@freeze_time("2024-03-15 15:01:00", tick=True)
@pytest.mark.order(7)
def test_served_topic_model_predict_sentiment(test_inference_params, test_new_es_index):
    """Tests ServedTopicModel's predict method without trend detection."""
    served_topic_model = ServedTopicModel()
    served_topic_model.load()
    with patch.object(
        served_topic_model.trend_detector, "es_index", new=test_new_es_index
    ), patch.object(
        served_topic_model.document_collector, "es_index", new=test_new_es_index
    ), patch.object(
        served_topic_model.impact_quantifier, "es_index", new=test_new_es_index
    ):

        test_input = PredictRequestSchema.from_data(
            namespace=settings.model_name,
            parameters=test_inference_params,
            attributes={
                "query_string": """((amex OR "american express" OR americanexpress) AND NOT ("nyse amex" OR "stade amex" OR abonnez-vous OR "American Express Global Business Travel" OR "american express gbt" OR "amex gbt" OR "amex global business travel" OR "William Muller" OR Sarrebourg )) OR "aXHH-Hotel hub" OR Euraxo OR aXcent OR "Carte Optima" OR "Carte SBS" OR "Carte Blue" OR Uvet OR Mobilextend OR Resoclub OR Resoclick OR Pcard OR "Nathalie Estrada" OR "Eric Tredjeu" OR "Sophie Janvier" OR "Cathy Notlet" OR "Claudine Hameau" OR "Stéphanie Laroque" OR "PF Brezes" OR "Hervé Sedky" OR "Gabrielle Elbaz" OR "Yves Pechon" OR  "Christophe Haviland" OR "Espace Voyages professionnels" OR Tripcase""",  # noqa: E501
                "topic_id": 19,
                "sentiment_impact_flag": True,
            },
        )
        test_actual_predict_output = served_topic_model.predict(test_input)
        assert test_actual_predict_output.attributes.topic is not None


@pytest.mark.order(8)
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
