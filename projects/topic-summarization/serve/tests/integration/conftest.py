# isort: skip_file
"""Conftest."""

# 3rd party libraries
import pytest
from fastapi.testclient import TestClient

# Internal libraries
from onclusiveml.serving.rest.serve import ServingParams

# Source
from src.serve.schema import BioResponseSchema
from src.serve.__main__ import get_model_server


@pytest.fixture
def test_serving_params():
    """Serving params fixture."""
    return ServingParams()


@pytest.fixture
def test_inference_params() -> str:
    """Predict parameter fixture."""
    return {}


@pytest.fixture
def test_new_es_index():
    """Mock es index."""
    new_es_index = [
        "crawler-4-2024.03",
        "crawler-4-2024.02",
        "crawler-4-2024.01",
        "crawler-4-2023.12",
        "crawler",
    ]
    return new_es_index


@pytest.fixture
def test_media_api_es_index():
    """Mock media api es index."""
    new_es_index = [
        "crawler-4-2024.07",
        "crawler-5-2024.06",
        "crawler",
    ]
    return new_es_index


@pytest.fixture
def test_media_api_query():
    """Input media api query."""
    return """{
            "query": {
                "simple": {
                    "terms": "(\\"biden\\")",
                    "case_sensitive_terms": None,
                    "operator": "and",
                    "search_fields": ["content", "title", "author"]
                }
            },
            "source": "360",
            "limit": 100,
            "page": 1,
            "filters": {
                "date": {
                    "start": "2024-06-15 16:09",
                    "end": "2024-07-15 18:09",
                    "time_zone": "+00:00"
                },
                "lang": [],
                "pagerank": {
                    "min": 0,
                    "max": 10
                },
                "country": ["GBR"],
                "domains": [],
                "relevance": {
                    "min": 0
                },
                "es_filter": {
                    "must_not": [
                        {
                            "multi_match": {
                                "query": "stocks",
                                "type": "cross_fields",
                                "fields": ["title", "content"],
                                "operator": "and",
                                "minimum_should_match": 3
                            }
                        },
                        {
                            "bool": {
                                "minimum_should_match": 2,
                                "should": [
                                    {
                                        "multi_match": {
                                            "query": "NYSE",
                                            "type": "cross_fields",
                                            "fields": ["title", "content"],
                                            "operator": "and"
                                        }
                                    },
                                    {
                                        "multi_match": {
                                            "query": "nasdaq",
                                            "type": "cross_fields",
                                            "fields": ["title", "content"],
                                            "operator": "and"
                                        }
                                    },
                                    {
                                        "multi_match": {
                                            "query": "DJIA",
                                            "type": "cross_fields",
                                            "fields": ["title", "content"],
                                            "operator": "and"
                                        }
                                    },
                                    {
                                        "multi_match": {
                                            "query": "S&P",
                                            "type": "cross_fields",
                                            "fields": ["title", "content"],
                                            "operator": "and"
                                        }
                                    },
                                    {
                                        "multi_match": {
                                            "query": "stock pick",
                                            "type": "phrase",
                                            "fields": ["title", "content"],
                                            "slop": 0
                                        }
                                    },
                                    {
                                        "multi_match": {
                                            "query": "stock performance",
                                            "type": "phrase",
                                            "fields": ["title", "content"],
                                            "slop": 0
                                        }
                                    },
                                    {
                                        "multi_match": {
                                            "query": "stock investor",
                                            "type": "phrase",
                                            "fields": ["title", "content"],
                                            "slop": 0
                                        }
                                    },
                                    {
                                        "multi_match": {
                                            "query": "stock market",
                                            "type": "phrase",
                                            "fields": ["title", "content"],
                                            "slop": 0
                                        }
                                    },
                                    {
                                        "multi_match": {
                                            "query": "stock price",
                                            "type": "phrase",
                                            "fields": ["title", "content"],
                                            "slop": 0
                                        }
                                    },
                                    {
                                        "multi_match": {
                                            "query": "stock prices",
                                            "type": "phrase",
                                            "fields": ["title", "content"],
                                            "slop": 0
                                        }
                                    },
                                    {
                                        "multi_match": {
                                            "query": "earnings snapshot",
                                            "type": "phrase",
                                            "fields": ["title", "content"],
                                            "slop": 0
                                        }
                                    },
                                    {
                                        "multi_match": {
                                            "query": "Dow jones",
                                            "type": "phrase",
                                            "fields": ["title", "content"],
                                            "slop": 0
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            },
            "exclude": {
                "country": [],
                "domains": ["metabase.moreover.com", "nyt.com"]
            },
            "sort": [
                {
                    "published_on": {
                        "order": "desc"
                    }
                }
            ],
            "profile_uuid": "be8d4f51-790f-4d22-9ec8-dc0a9b41e9de",
            "return_fields": [
                "id", "ave", "amplification", "author", "country", "domain", "lang", "publication", "published_on", "reach", "summary", "title", "url", "score", "media_type", "pagerank", "licenses", "publication_details", "sentiment", "author_id", "thumbnail_url", "metadata"
            ],
            "media_types": ["print"]
        }"""  # noqa: E501


@pytest.fixture
def test_client():
    """Client fixture."""
    model_server = get_model_server()

    return TestClient(model_server)


@pytest.fixture
def test_predict_input() -> str:
    """Predict input fixture."""
    return [
        """
            India's semiconductor component market will see its cumulative revenues climb to $300 billion during 2021-2026,
            a report said Tuesday. The ‘India Semiconductor Market Report, 2019-2026',
            a joint research by the India Electronics & Semiconductor Association (IESA) and Counterpoint Research,
            observed that India is poised to be the second largest market in the world in terms of scale and growing demand for
            semiconductor components across several industries and applications.
            It added that this was being bolstered by the increasing pace of digital transformation and the adoption of
            new technologies and covers smartphones, PCs, wearables, cloud data centers,
            Industry 4.0 applications, IoT, smart mobility, and advanced telecom and public utility infrastructure.
            “While the country is becoming one of the largest consumers of electronic and semiconductor components,
            most components are imported, offering limited economic opportunities for the country.
            Currently, only 9% of this semiconductor requirement is met locally,” the report said.
            it noted that India's end equipment market in 2021 stood at $119 billion in terms of revenue and
            is expected to grow at a CAGR of 19% from 2021 to 2026.
            It said that the Electronic System Design and Manufacturing (ESDM) sector in India will play a major role in the
            country's overall growth, from sourcing components to design manufacturing.
            “Before the end of this decade, there will be nothing that will not be touched by electronics and the ubiquitous ‘chip,
            '” IESA CEO Krishna Moorthy said. “Be it fighting carbon emissions, renewable energy, food safety, or healthcare,
            the semiconductor chip will be all-pervasive.""",  # noqa: E501
        """
            Scientists are particularly excited to finally have images of two black holes of very different sizes, which offers the
            opportunity to understand how they compare and contrast.  They have also begun to use the new data to test theories and models
            of how gas behaves around supermassive black holes. This process is not yet fully understood but is thought to play a key role
            in shaping the formation and evolution of galaxies.'
        """,  # noqa: E501
    ]


@pytest.fixture
def test_model_name() -> str:
    """Test model name fixture."""
    return "topic-summarization"


@pytest.fixture
def test_expected_bio_output(test_model_name):
    """Test expected bio output."""
    return BioResponseSchema.from_data(
        version=1,
        namespace="topic-summarization",
        attributes={"model_name": "topic-summarization"},
    )
