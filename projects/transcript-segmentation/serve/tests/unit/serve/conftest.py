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
        {"hl": False, "index": 0, "textId": None, "w": None, "ts": 1701127800000},
        {"hl": False, "index": 1, "textId": None, "w": None, "ts": 1701127801000},
        {"hl": False, "index": 2, "textId": None, "w": None, "ts": 1701127802000},
        {"hl": False, "index": 3, "textId": None, "w": None, "ts": 1701127803000},
        {"hl": False, "index": 4, "textId": None, "w": None, "ts": 1701127804000},
        {"hl": False, "index": 5, "textId": None, "w": None, "ts": 1701127805000},
        {"hl": False, "index": 6, "textId": None, "w": None, "ts": 1701127806000},
        {"hl": False, "index": 7, "textId": None, "w": None, "ts": 1701127807000},
        {"hl": False, "index": 8, "textId": None, "w": None, "ts": 1701127808000},
        {"hl": False, "index": 9, "textId": None, "w": None, "ts": 1701127809000},
        {"hl": False, "index": 10, "textId": None, "w": None, "ts": 1701127810000},
        {"hl": False, "index": 11, "textId": None, "w": None, "ts": 1701127811000},
        {"hl": False, "index": 12, "textId": None, "w": None, "ts": 1701127812000},
        {"hl": False, "index": 13, "textId": None, "w": None, "ts": 1701127813000},
        {"hl": False, "index": 14, "textId": None, "w": None, "ts": 1701127814000},
        {"hl": False, "index": 15, "textId": None, "w": None, "ts": 1701127815000},
        {"ts": 1701127816000.0, "w": "Watch", "index": 16},
        {"ts": 1701127816500.0, "w": "'a", "index": 17},
        {"ts": 1701127817000.0, "w": "Day's", "index": 18},
        {"ts": 1701127817500.0, "w": "Work,'", "index": 19},
        {"ts": 1701127818000.0, "w": "in", "index": 20},
        {"ts": 1701127818666.6667, "w": "their", "index": 21},
        {"ts": 1701127819333.3333, "w": "unreliability.", "index": 22},
        {"ts": 1701127820000.0, "w": "They're", "index": 23},
        {"ts": 1701127820285.7144, "w": "arguably", "index": 24},
        {"ts": 1701127820571.4285, "w": "the", "index": 25},
        {"ts": 1701127820857.1428, "w": "most", "index": 26},
        {"ts": 1701127821142.8572, "w": "versatile", "index": 27},
        {"ts": 1701127821428.5715, "w": "ai", "index": 28},
        {"ts": 1701127821714.2856, "w": "technique", "index": 29},
        {"ts": 1701127822000.0, "w": "that's", "index": 30},
        {"ts": 1701127822500.0, "w": "ever", "index": 31},
        {"ts": 1701127823000.0, "w": "been", "index": 32},
        {"ts": 1701127823500.0, "w": "developed,", "index": 33},
        {"ts": 1701127824000.0, "w": "but", "index": 34},
        {"ts": 1701127824250.0, "w": "they're", "index": 35},
        {"ts": 1701127824500.0, "w": "also", "index": 36},
        {"ts": 1701127824750.0, "w": "the", "index": 37},
        {"ts": 1701127825000.0, "w": "least", "index": 38},
        {"ts": 1701127825250.0, "w": "reliable", "index": 39},
        {"ts": 1701127825500.0, "w": "ai", "index": 40},
        {"ts": 1701127825750.0, "w": "technique", "index": 41},
        {"ts": 1701127826000.0, "w": "that's", "index": 42},
        {"ts": 1701127826500.0, "w": "ever", "index": 43},
        {"ts": 1701127827000.0, "w": "gone", "index": 44},
        {"ts": 1701127827500.0, "w": "mainstream.", "index": 45},
        {"ts": 1701127828000.0, "w": "[bright", "index": 46},
        {"ts": 1701127832000.0, "w": "music]", "index": 47},
        {"ts": 1701127836000.0, "w": "[logo", "index": 48},
        {"ts": 1701127836500.0, "w": "whooshes]", "index": 49},
        {"ts": 1701127837000.0, "w": "-", "index": 50},
        {"ts": 1701127837285.7144, "w": "Hello", "index": 51},
        {"ts": 1701127837571.4285, "w": "and", "index": 52},
        {"ts": 1701127837857.1428, "w": "welcome", "index": 53},
        {"ts": 1701127838142.8572, "w": "to", "index": 54},
        {"ts": 1701127838428.5715, "w": '"gzero', "index": 55},
        {"ts": 1701127838714.2856, "w": "World.", "index": 56},
        {"ts": 1701127839000.0, "w": "I'm", "index": 57},
        {"ts": 1701127839600.0, "w": "Ian", "index": 58},
        {"ts": 1701127840200.0, "w": "Bremmer,", "index": 59},
        {"ts": 1701127840800.0, "w": "and,", "index": 60},
        {"ts": 1701127841400.0, "w": "today,", "index": 61},
        {"ts": 1701127842000.0, "w": "we're", "index": 62},
        {"ts": 1701127842428.5715, "w": "talking", "index": 63},
        {"ts": 1701127842857.1428, "w": "about", "index": 64},
        {"ts": 1701127843285.7144, "w": "all", "index": 65},
        {"ts": 1701127843714.2856, "w": "things", "index": 66},
        {"ts": 1701127844142.8572, "w": "artificial", "index": 67},
        {"ts": 1701127844571.4285, "w": "intelligence,", "index": 68},
        {"ts": 1701127845000.0, "w": "specifically", "index": 69},
        {"ts": 1701127845285.7144, "w": "generative", "index": 70},
        {"ts": 1701127845571.4285, "w": "ai,", "index": 71},
        {"ts": 1701127845857.1428, "w": "those", "index": 72},
        {"ts": 1701127846142.8572, "w": "chatbots", "index": 73},
        {"ts": 1701127846428.5715, "w": "like", "index": 74},
        {"ts": 1701127846714.2856, "w": "ChatGPT", "index": 75},
        {"ts": 1701127847000.0, "w": "that", "index": 76},
        {"ts": 1701127847285.7144, "w": "you've", "index": 77},
        {"ts": 1701127847571.4285, "w": "surely", "index": 78},
        {"ts": 1701127847857.1428, "w": "heard", "index": 79},
        {"ts": 1701127848142.8572, "w": "about", "index": 80},
        {"ts": 1701127848428.5715, "w": "by", "index": 81},
        {"ts": 1701127848714.2856, "w": "now.", "index": 82},
        {"ts": 1701127849000.0, "w": "You", "index": 83},
        {"ts": 1701127849375.0, "w": "know,", "index": 84},
        {"ts": 1701127849750.0, "w": "the", "index": 85},
        {"ts": 1701127850125.0, "w": "ones", "index": 86},
        {"ts": 1701127850500.0, "w": "that", "index": 87},
        {"ts": 1701127850875.0, "w": "can", "index": 88},
        {"ts": 1701127851250.0, "w": "churn", "index": 89},
        {"ts": 1701127851625.0, "w": "out", "index": 90},
        {"ts": 1701127852000.0, "w": "a", "index": 91},
        {"ts": 1701127852142.8572, "w": "two-hour", "index": 92},
        {"ts": 1701127852285.7144, "w": "movie", "index": 93},
        {"ts": 1701127852428.5715, "w": "script", "index": 94},
        {"ts": 1701127852571.4285, "w": "or", "index": 95},
        {"ts": 1701127852714.2856, "w": "Picasso-style", "index": 96},
        {"ts": 1701127852857.1428, "w": "painting", "index": 97},
        {"ts": 1701127853000.0, "w": "in", "index": 98},
        {"ts": 1701127853750.0, "w": "just", "index": 99},
        {"ts": 1701127854500.0, "w": "an", "index": 100},
        {"ts": 1701127855250.0, "w": "instant.", "index": 101},
        {"ts": 1701127856000.0, "w": "With", "index": 102},
        {"ts": 1701127856571.4285, "w": "the", "index": 103},
        {"ts": 1701127857142.8572, "w": "recent", "index": 104},
        {"ts": 1701127857714.2856, "w": "rollout", "index": 105},
        {"ts": 1701127858285.7144, "w": "of", "index": 106},
        {"ts": 1701127858857.1428, "w": "OpenAI's", "index": 107},
        {"ts": 1701127859428.5715, "w": "ChatGPT-4,", "index": 108},
    ]  # noqa: E501


@pytest.fixture
def expected_output():
    """Expect output from predict."""
    return {
        "start_time": 1701127820000,
        "end_time": 1701127849000,
        "input_truncated": False,
    }
