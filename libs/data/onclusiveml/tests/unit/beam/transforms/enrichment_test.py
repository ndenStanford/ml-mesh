"""Enrichment test."""

# Standard Library
from unittest.mock import patch

# 3rd party libraries
import apache_beam as beam
import pytest
from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.util import assert_that, equal_to
from pydantic import SecretStr

# Internal libraries
from onclusiveml.data.beam.transforms.enrichment import (
    MachineLearningEnrichment,
)


@pytest.mark.parametrize(
    "host, api_key, api, in_keys, request_json, response_json, expected",
    [
        (
            "example.com",
            "",
            "entity_linking",
            ["content", "lang", "entities"],
            [
                (
                    "key",
                    {
                        "content": "Onclusive is a media monitoring company",
                        "lang": "en",
                        "entities": [],
                    },
                )
            ],
            {
                "version": 1,
                "data": {
                    "identifier": None,
                    "namespace": "entity-linking",
                    "attributes": {
                        "entities": [
                            {
                                "entity_type": "ORG",
                                "entity_text": "Onclusive",
                                "score": 0.9571336805820465,
                                "sentence_index": 0,
                                "wiki_link": None,
                            }
                        ]
                    },
                },
            },
            [
                (
                    "key",
                    {
                        "content": "Onclusive is a media monitoring company",
                        "lang": "en",
                        "entities": [],
                        "entity_linking": {
                            "entities": [
                                {
                                    "entity_type": "ORG",
                                    "entity_text": "Onclusive",
                                    "score": 0.9571336805820465,
                                    "sentence_index": 0,
                                    "wiki_link": None,
                                }
                            ]
                        },
                    },
                )
            ],
        ),
        (
            "example.com",
            "",
            "ner",
            ["content", "language"],
            [
                (
                    "key",
                    {
                        "content": "Onclusive is a media monitoring company",
                        "language": "en",
                    },
                )
            ],
            {
                "version": 1,
                "data": {
                    "identifier": None,
                    "namespace": "ner",
                    "attributes": {
                        "entities": [
                            {
                                "entity_type": "ORG",
                                "entity_text": "Onclusive",
                                "score": 0.8461078107357025,
                                "sentence_index": 0,
                                "start": 0,
                                "end": 9,
                            }
                        ]
                    },
                },
            },
            [
                (
                    "key",
                    {
                        "content": "Onclusive is a media monitoring company",
                        "language": "en",
                        "ner": {
                            "entities": [
                                {
                                    "entity_type": "ORG",
                                    "entity_text": "Onclusive",
                                    "score": 0.8461078107357025,
                                    "sentence_index": 0,
                                    "start": 0,
                                    "end": 9,
                                }
                            ]
                        },
                    },
                )
            ],
        ),
    ],
)
@patch("requests.request")
def test_api_call_dofn(
    mock_request, host, api_key, api, in_keys, request_json, response_json, expected
):
    """Test api call DoFn."""
    mock_request.return_value.status_code = 200
    mock_request.return_value.json.return_value = response_json

    with TestPipeline() as pipeline:
        result = (
            pipeline
            | "Start" >> beam.Create(request_json)
            | "Do"
            >> MachineLearningEnrichment(
                host=host,
                api_key=SecretStr(""),
                secure=True,
                namespace=api,
                version=1,
                in_keys=in_keys,
            )
        )
        assert_that(result, equal_to(expected))
