"""Conftest."""

# 3rd party libraries
import pytest

# Source
from src.settings import get_settings


@pytest.fixture(scope="function")
def settings():
    """Settings fixture."""
    return get_settings()


@pytest.fixture
def test_payload():
    """Payload."""
    return {
        "data": {
            "identifier": "string",
            "namespace": "transcript-segmentation",
            "attributes": {
                "transcript": [
                    {
                        "hl": False,
                        "index": 0,
                        "textId": None,
                        "w": None,
                        "ts": 1701127800000,
                    },
                    {
                        "hl": False,
                        "index": 1,
                        "textId": None,
                        "w": None,
                        "ts": 1701127801000,
                    },
                    {
                        "hl": False,
                        "index": 2,
                        "textId": None,
                        "w": None,
                        "ts": 1701127802000,
                    },
                    {
                        "hl": False,
                        "index": 3,
                        "textId": None,
                        "w": None,
                        "ts": 1701127803000,
                    },
                    {
                        "hl": False,
                        "index": 4,
                        "textId": None,
                        "w": None,
                        "ts": 1701127804000,
                    },
                    {
                        "hl": False,
                        "index": 5,
                        "textId": None,
                        "w": None,
                        "ts": 1701127805000,
                    },
                    {
                        "hl": False,
                        "index": 6,
                        "textId": None,
                        "w": None,
                        "ts": 1701127806000,
                    },
                    {
                        "hl": False,
                        "index": 7,
                        "textId": None,
                        "w": None,
                        "ts": 1701127807000,
                    },
                    {
                        "hl": False,
                        "index": 8,
                        "textId": None,
                        "w": None,
                        "ts": 1701127808000,
                    },
                    {
                        "hl": False,
                        "index": 9,
                        "textId": None,
                        "w": None,
                        "ts": 1701127809000,
                    },
                    {
                        "hl": False,
                        "index": 10,
                        "textId": None,
                        "w": None,
                        "ts": 1701127810000,
                    },
                    {
                        "hl": False,
                        "index": 11,
                        "textId": None,
                        "w": None,
                        "ts": 1701127811000,
                    },
                    {
                        "hl": False,
                        "index": 12,
                        "textId": None,
                        "w": None,
                        "ts": 1701127812000,
                    },
                    {
                        "hl": False,
                        "index": 13,
                        "textId": None,
                        "w": None,
                        "ts": 1701127813000,
                    },
                    {
                        "hl": False,
                        "index": 14,
                        "textId": None,
                        "w": None,
                        "ts": 1701127814000,
                    },
                    {
                        "hl": False,
                        "index": 15,
                        "textId": None,
                        "w": None,
                        "ts": 1701127815000,
                    },
                    {
                        "start_time": 1701127816000.0,
                        "content": "Watch 'a Day's Work,' in their unreliability.",
                    },
                    {
                        "start_time": 1701127820000.0,
                        "content": "They're arguably the most versatile ai technique that's ever been developed, but they're also the least reliable ai technique that's ever gone mainstream.",  # noqa: E501
                    },  # noqa: E501
                    {
                        "start_time": 1701127828000.0,
                        "content": '[bright music] [logo whooshes] - Hello and welcome to "gzero World.',  # noqa: E501
                    },  # noqa: E501
                    {
                        "start_time": 1701127839000.0,
                        "content": "I'm Ian Bremmer, and, today, we're talking about all things artificial intelligence, specifically generative ai, those chatbots like ChatGPT that you've surely heard about by now.",  # noqa: E501
                    },  # noqa: E501
                    {
                        "start_time": 1701127849000.0,
                        "content": "You know, the ones that can churn out a two-hour movie script or Picasso-style painting in just an instant.",  # noqa: E501
                    },  # noqa: E501
                ],
                "keywords": ["Ai"],
            },
            "parameters": {},
        }
    }


@pytest.fixture
def expected_response():
    """Expect response from API."""
    return {
        "version": 1,
        "data": {
            "identifier": None,
            "namespace": "transcript-segmentation",
            "attributes": {
                "start_time": 1701127839000.0,
                "end_time": 1701127848714.0,
                "input_truncated": False,
                "summary": None,
            },
        },
    }
