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
    mock_response.content = """{"generated": "{\\n    \\"Related segment\\": \\"They\'re arguably the most versatile ai technique that\'s ever been developed, but they\'re also the least reliable ai technique that\'s ever gone mainstream. [bright music] [logo whooshes] - Hello and welcome to \\\\\\"gzero World. I\'m Ian Bremmer, and, today, we\'re talking about all things artificial intelligence, specifically generative ai, those chatbots like ChatGPT that you\'ve surely heard about by now. You know, the ones that can churn out a two-hour movie script or Picasso-style painting in just an instant. With the recent rollout of OpenAI\'s ChatGPT-4,\\",\\n    \\"Reason for segment\\": \\"This segment is directly related to the keyword \'Ai\' as it discusses the versatility and reliability of ai techniques, mentions artificial intelligence, generative ai, and specifically refers to ChatGPT, which is an example of an Ai application.\\",\\n    \\"Reason for no segment\\": \\"N/A\\"\\n}"}"""  # noqa
    return mock_response


@pytest.fixture
def transcript_keywords():
    """Input keyword."""
    return ["Ai"]


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
        "start_time": 1701127816000.0,
        "end_time": 1701127859428.5715,
        "transcript_start_time": 1701127820000,
        "transcript_end_time": 1701127859428.5715,
    }


@pytest.fixture
def expected_preprocessing_output():
    """Expected preprocessing output."""
    return [
        {
            "content": "Watch 'a Day's Work,' in their unreliability.",
            "end_time": 1701127819333.3333,
            "start_time": 1701127816000.0,
        },
        {
            "content": "They're arguably the most versatile ai technique that's ever been developed, but they're also the least reliable ai technique that's ever gone mainstream.",  # noqa: E501
            "end_time": 1701127827500.0,
            "start_time": 1701127820000.0,
        },
        {
            "content": '[bright music] [logo whooshes] - Hello and welcome to "gzero World.',
            "end_time": 1701127838714.2856,
            "start_time": 1701127828000.0,
        },
        {
            "content": "I'm Ian Bremmer, and, today, we're talking about all things artificial intelligence, specifically generative ai, those chatbots like ChatGPT that you've surely heard about by now.",  # noqa: E501
            "end_time": 1701127848714.2856,
            "start_time": 1701127839000.0,
        },
        {
            "content": "You know, the ones that can churn out a two-hour movie script or Picasso-style painting in just an instant.",  # noqa: E501
            "end_time": 1701127855250.0,
            "start_time": 1701127849000.0,
        },
        {
            "content": "With the recent rollout of OpenAI's ChatGPT-4,",
            "end_time": 1701127859428.5715,
            "start_time": 1701127856000.0,
        },
    ]


@pytest.fixture
def transcript_input_abbrv():
    """Input transcript with abbreviation."""
    return [
        {"ts": 1706450460000.0, "w": "A", "index": 0, "textId": ""},
        {"ts": 1706450460200.0, "w": "judge", "index": 1, "textId": ""},
        {"ts": 1706450460400.0, "w": "in", "index": 2, "textId": ""},
        {"ts": 1706450460600.0, "w": "Los", "index": 3, "textId": ""},
        {"ts": 1706450460800.0, "w": "Angeles", "index": 4, "textId": ""},
        {"ts": 1706450461000.0, "w": "has", "index": 5, "textId": ""},
        {"ts": 1706450461166.6667, "w": "ordered", "index": 6, "textId": ""},
        {"ts": 1706450461333.3333, "w": "police", "index": 7, "textId": ""},
        {"ts": 1706450461500.0, "w": "not", "index": 8, "textId": ""},
        {"ts": 1706450461666.6667, "w": "to", "index": 9, "textId": ""},
        {"ts": 1706450461833.3333, "w": "reveal", "index": 10, "textId": ""},
        {"ts": 1706450462000.0, "w": "what", "index": 11, "textId": ""},
        {"ts": 1706450462250.0, "w": "they", "index": 12, "textId": ""},
        {"ts": 1706450462500.0, "w": "found", "index": 13, "textId": ""},
        {"ts": 1706450462750.0, "w": "when", "index": 14, "textId": ""},
        {"ts": 1706450463000.0, "w": "they", "index": 15, "textId": ""},
        {"ts": 1706450463333.3333, "w": "raided", "index": 16, "textId": ""},
        {"ts": 1706450463666.6667, "w": "the", "index": 17, "textId": ""},
        {"ts": 1706450464000.0, "w": "home", "index": 18, "textId": ""},
        {"ts": 1706450464200.0, "w": "of", "index": 19, "textId": ""},
        {"ts": 1706450464400.0, "w": "an", "index": 20, "textId": ""},
        {"ts": 1706450464600.0, "w": "attorney", "index": 21, "textId": ""},
        {"ts": 1706450464800.0, "w": "representing", "index": 22, "textId": ""},
        {"ts": 1706450465000.0, "w": "Black", "index": 23, "textId": ""},
        {"ts": 1706450465166.6667, "w": "Lives", "index": 24, "textId": ""},
        {"ts": 1706450465333.3333, "w": "Matter.", "index": 25, "textId": ""},
        {"ts": 1706450465500.0, "w": "Officers", "index": 26, "textId": ""},
        {"ts": 1706450465666.6667, "w": "from", "index": 27, "textId": ""},
        {"ts": 1706450465833.3333, "w": "L.", "index": 28, "textId": ""},
        {"ts": 1706450466000.0, "w": "A.", "index": 29, "textId": ""},
        {"ts": 1706450466142.8572, "w": "P.", "index": 30, "textId": ""},
        {"ts": 1706450466285.7144, "w": "D.", "index": 31, "textId": ""},
        {"ts": 1706450466428.5715, "w": "took", "index": 32, "textId": ""},
        {"ts": 1706450466571.4285, "w": "photos", "index": 33, "textId": ""},
        {"ts": 1706450466714.2856, "w": "in", "index": 34, "textId": ""},
        {"ts": 1706450466857.1428, "w": "the", "index": 35, "textId": ""},
        {"ts": 1706450467000.0, "w": "house", "index": 36, "textId": ""},
        {"ts": 1706450467200.0, "w": "of", "index": 37, "textId": ""},
        {"ts": 1706450467400.0, "w": "Dermot", "index": 38, "textId": ""},
        {"ts": 1706450467600.0, "w": "Givens", "index": 39, "textId": ""},
        {"ts": 1706450467800.0, "w": "on", "index": 40, "textId": ""},
        {"ts": 1706450468000.0, "w": "Tuesday", "index": 41, "textId": ""},
        {"ts": 1706450468333.3333, "w": "as", "index": 42, "textId": ""},
        {"ts": 1706450468666.6667, "w": "they", "index": 43, "textId": ""},
        {"ts": 1706450469000.0, "w": "hunted", "index": 44, "textId": ""},
        {"ts": 1706450469166.6667, "w": "for", "index": 45, "textId": ""},
        {"ts": 1706450469333.3333, "w": "a", "index": 46, "textId": ""},
        {"ts": 1706450469500.0, "w": "suspect", "index": 47, "textId": ""},
        {"ts": 1706450469666.6667, "w": "they", "index": 48, "textId": ""},
        {"ts": 1706450469833.3333, "w": "were", "index": 49, "textId": ""},
        {"ts": 1706450470000.0, "w": "following", "index": 50, "textId": ""},
        {"ts": 1706450470250.0, "w": "via", "index": 51, "textId": ""},
        {"ts": 1706450470500.0, "w": "an", "index": 52, "textId": ""},
        {"ts": 1706450470750.0, "w": "AirTag", "index": 53, "textId": ""},
        {"ts": 1706450471000.0, "w": "tracking", "index": 54, "textId": ""},
        {"ts": 1706450471200.0, "w": "device.", "index": 55, "textId": ""},
        {"ts": 1706450471400.0, "w": "Givens", "index": 56, "textId": ""},
        {"ts": 1706450471600.0, "w": "claimed", "index": 57, "textId": ""},
        {"ts": 1706450471800.0, "w": "the", "index": 58, "textId": ""},
        {"ts": 1706450472000.0, "w": "snaps", "index": 59, "textId": ""},
        {"ts": 1706450472200.0, "w": "included", "index": 60, "textId": ""},
        {"ts": 1706450472400.0, "w": "legal", "index": 61, "textId": ""},
        {"ts": 1706450472600.0, "w": "documents", "index": 62, "textId": ""},
        {"ts": 1706450472800.0, "w": "concerning", "index": 63, "textId": ""},
        {"ts": 1706450473000.0, "w": "BLM", "index": 64, "textId": ""},
        {"ts": 1706450473200.0, "w": "leader", "index": 65, "textId": ""},
        {"ts": 1706450473400.0, "w": "Melina", "index": 66, "textId": ""},
        {"ts": 1706450473600.0, "w": "Abdullah,", "index": 67, "textId": ""},
        {"ts": 1706450473800.0, "w": "who", "index": 68, "textId": ""},
        {"ts": 1706450474000.0, "w": "is", "index": 69, "textId": ""},
        {"ts": 1706450474200.0, "w": "suing", "index": 70, "textId": ""},
        {"ts": 1706450474400.0, "w": "the", "index": 71, "textId": ""},
        {"ts": 1706450474600.0, "w": "department", "index": 72, "textId": ""},
        {"ts": 1706450474800.0, "w": "after", "index": 73, "textId": ""},
        {"ts": 1706450475000.0, "w": "they", "index": 74, "textId": ""},
        {"ts": 1706450475200.0, "w": "descended", "index": 75, "textId": ""},
        {"ts": 1706450475400.0, "w": "on", "index": 76, "textId": ""},
        {"ts": 1706450475600.0, "w": "her", "index": 77, "textId": ""},
        {"ts": 1706450475800.0, "w": "$1.6million", "index": 78, "textId": ""},
        {"ts": 1706450476000.0, "w": "home", "index": 79, "textId": ""},
        {"ts": 1706450476500.0, "w": "in", "index": 80, "textId": ""},
        {"ts": 1706450477000.0, "w": "2020", "index": 81, "textId": ""},
        {"ts": 1706450477333.3333, "w": "in", "index": 82, "textId": ""},
        {"ts": 1706450477666.6667, "w": "response", "index": 83, "textId": ""},
        {"ts": 1706450478000.0, "w": "to", "index": 84, "textId": ""},
        {"ts": 1706450478166.6667, "w": "a", "index": 85, "textId": ""},
        {"ts": 1706450478333.3333, "w": "reported", "index": 86, "textId": ""},
        {"ts": 1706450478500.0, "w": "swatting", "index": 87, "textId": ""},
        {"ts": 1706450478666.6667, "w": "incident.", "index": 88, "textId": ""},
    ]


@pytest.fixture
def expected_preprocessing_output_abbrv():
    """Expected preprocessing output with abbreviation."""
    return [
        {
            "content": "A judge in Los Angeles has ordered police not to reveal what they found when they raided the home of an attorney representing Black Lives Matter.",  # noqa: E501
            "end_time": 1706450465333.3333,
            "start_time": 1706450460000.0,
        },
        {
            "content": "Officers from L.A.P.D. took photos in the house of Dermot Givens on Tuesday as they hunted for a suspect they were following via an AirTag tracking device.",  # noqa: E501
            "end_time": 1706450471200.0,
            "start_time": 1706450465500.0,
        },
        {
            "content": "Givens claimed the snaps included legal documents concerning BLM leader Melina Abdullah, who is suing the department after they descended on her $1.6million home in 2020 in response to a reported swatting incident.",  # noqa: E501
            "end_time": 1706450478666.6667,
            "start_time": 1706450471400.0,
        },
    ]
