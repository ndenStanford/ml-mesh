"""Model test."""

# Standard Library
from unittest.mock import patch

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.models.sentiment import CompiledSent

# Source
from src.serve.artifacts import ServedModelArtifacts
from src.serve.model import ServedSentModel
from src.serve.schemas import PredictRequestSchema, PredictResponseSchema


def test_served_model_init(served_model):
    """Test served model initialization."""
    assert isinstance(served_model.served_model_artifacts, ServedModelArtifacts)
    assert not served_model.ready


@patch.object(CompiledSent, "from_pretrained")
def test_served_model_load(mock_from_pretrained, served_model):
    """Test served model load."""
    assert not served_model.ready
    served_model.load()
    assert served_model.ready

    mock_from_pretrained.assert_called_with(
        served_model.served_model_artifacts.model_artifact_directory
    )


# @pytest.mark.parametrize(
#     "payload, predict_return, expected_response",
#     [
#         (
#             {
#                 "data": {
#                     "namespace": "sentiment",
#                     "attributes": {
#                         "content": "London is a wonderful city. Anna is a terrible person."
#                     },
#                     "parameters": {
#                         "entities": [
#                             {
#                                 "entity_type": "PER",
#                                 "entity_text": "Anna",
#                                 "score": "0.9987269",
#                                 "sentence_index": 1,
#                                 "start": 0,
#                                 "end": 4,
#                             },
#                             {
#                                 "entity_type": "LOC",
#                                 "entity_text": "London",
#                                 "score": "0.99966383",
#                                 "sentence_index": 0,
#                                 "start": 0,
#                                 "end": 6,
#                             },
#                         ],
#                         "language": "en",
#                     },
#                 }
#             },
#             {
#                 "label": "positive",
#                 "negative_prob": 0.488,
#                 "positive_prob": 0.4776,
#                 "entities": [
#                     {
#                         "entity_type": "LOC",
#                         "entity_text": "London",
#                         "score": 0.99966383,
#                         "sentence_index": 0,
#                         "start": 0,
#                         "end": 6,
#                         "sentiment": "positive",
#                     },
#                     {
#                         "entity_type": "PER",
#                         "entity_text": "Anna",
#                         "score": 0.9987269,
#                         "sentence_index": 1,
#                         "start": 0,
#                         "end": 4,
#                         "sentiment": "negative",
#                     },
#                 ],
#             },
#             {
#                 "version": 1,
#                 "data": {
#                     "namespace": "sentiment",
#                     "attributes": {
#                         "label": "positive",
#                         "negative_prob": 0.488,
#                         "positive_prob": 0.4776,
#                         "entities": [
#                             {
#                                 "entity_type": "LOC",
#                                 "entity_text": "London",
#                                 "score": 0.99966383,
#                                 "sentence_index": 0,
#                                 "start": 0,
#                                 "end": 6,
#                                 "sentiment": "positive",
#                             },
#                             {
#                                 "entity_type": "PER",
#                                 "entity_text": "Anna",
#                                 "score": 0.9987269,
#                                 "sentence_index": 1,
#                                 "start": 0,
#                                 "end": 4,
#                                 "sentiment": "negative",
#                             },
#                         ],
#                     },
#                 },
#             },
#         ),
#     ],
# )
# @patch.object(ServedSentModel, "model")
# @patch.object(CompiledSent, "from_pretrained")
# def test_served_model_predict(
#     from_pretrained_mock,
#     model_call_mock,
#     served_model,
#     payload,
#     predict_return,
#     expected_response,
# ):
#     """Test served model predict method."""
#     model_call_mock.return_value.inference.return_value = predict_return

#     served_model.load()
#     response = served_model.predict(PredictRequestSchema(**payload))

#     assert isinstance(response, PredictResponseSchema)

#     model_call_mock.assert_called_with(
#         sentences=[payload["data"]["attributes"]["content"]],
#         **payload["data"]["parameters"]
#     )

#     response.version == expected_response["version"]
#     response.data.identifier == expected_response["data"]["identifier"]
#     response.data.namespace == expected_response["data"]["namespace"]
#     response.data.attributes == expected_response["data"]["attributes"]


# @pytest.mark.parametrize(
#     "payload, predict_return, expected_response",
#     [
#         (
#             {
#                 "data": {
#                     "identifier": None,
#                     "namespace": "ner",
#                     "attributes": {"content": ""},
#                     "parameters": {"language": "en"},
#                 }
#             },
#             [],
#             {
#                 "version": 1,
#                 "data": {
#                     "identifier": None,
#                     "namespace": "ner",
#                     "attributes": {"entities": []},
#                 },
#             },
#         )
#     ],
# )
# @patch.object(CompiledNER, "__call__")
# @patch.object(CompiledNER, "from_pretrained")
# def test_served_model_predict_empty_content(
#     from_pretrained_mock,
#     model_call_mock,
#     served_model,
#     payload,
#     predict_return,
#     expected_response,
# ):
#     """Test served model predict method with empty content."""
#     model_call_mock.return_value = predict_return

#     served_model.load()
#     response = served_model.predict(PredictRequestSchema(**payload))

#     assert isinstance(response, PredictResponseSchema)

#     model_call_mock.assert_not_called()
