"""Conftest."""
# isort: skip_file

# Standard Library
from unittest.mock import MagicMock

# 3rd party libraries
import pytest

# Source


@pytest.fixture
def model_card():
    """Mock response for request.post."""
    mock_response = MagicMock()
    mock_response.content = """{"generated":"{\\n  \\"Relationship with keyword\\": \\"The transcript contains multiple mentions of \'AI\', which stands for artificial intelligence, and discusses aspects of generative AI and its applications.\\",\\n  \\"Related segment\\": {\\"start_time\\": 1701127820000.0, \\"end_time\\": 1701127849000.0},\\n  \\"Reason\\": \\"The selected segment is the most relevant because it discusses the versatility and reliability of AI techniques, introduces the topic of generative AI, and mentions specific examples of AI applications like ChatGPT and its ability to create content rapidly.\\",\\n  \\"Reason for not choose\\": \\"N/A as the transcript does contain relevant content related to the keyword \'Ai\'.\\"\\n}"}"""  # noqa
    return mock_response


@pytest.fixture
def transcript_keywords():
    """Input keyword."""
    return ["OpenAI"]


@pytest.fixture
def transcript_input():
    """Input transcript."""
    return [
        {
            "start_time": 1701127816000.0,
            "content": "Watch 'a Day's Work,' in their unreliability.",
        },
        {
            "start_time": 1701127820000.0,
            "content": "They're arguably the most versatile ai technique that's ever been developed, but they're also the least reliable ai technique that's ever gone mainstream.",  # noqa: E501
        },
        {
            "start_time": 1701127828000.0,
            "content": '[bright music] [logo whooshes] - Hello and welcome to "gzero World.',
        },
        {
            "start_time": 1701127839000.0,
            "content": "I'm Ian Bremmer, and, today, we're talking about all things artificial intelligence, specifically generative ai, those chatbots like ChatGPT that you've surely heard about by now.",  # noqa: E501
        },
        {
            "start_time": 1701127849000.0,
            "content": "You know, the ones that can churn out a two-hour movie script or Picasso-style painting in just an instant.",  # noqa: E501
        },
    ]  # noqa: E501


@pytest.fixture
def expected_output():
    """Expect output from predict."""
    return {
        "start_time": 1701127820000,
        "end_time": 1701127849000,
        "input_truncated": False,
    }
