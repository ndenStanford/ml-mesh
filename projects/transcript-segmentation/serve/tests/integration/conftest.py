"""Conftest."""

# Standard Library
from typing import List

# 3rd party libraries
import pytest
from fastapi.testclient import TestClient

# Internal libraries
from onclusiveml.serving.rest.serve import ServingParams

# Source
from src.serve.schemas import BioResponseSchema, PredictResponseSchema
from src.serve.server import model_server


@pytest.fixture
def test_serving_params():
    """Serving params fixture."""
    return ServingParams()


@pytest.fixture
def test_client():
    """Client fixture."""
    return TestClient(model_server)


@pytest.fixture
def test_predict_input_fr() -> str:
    """Predict input fixture in French."""
    return [
        {"ts": 1721029225000, "w": "tard.", "index": 456, "hl": None, "textId": ""},
        {"ts": 1721029225500, "w": "Devenez", "index": 457, "hl": None, "textId": ""},
        {"ts": 1721029226000, "w": "maître", "index": 458, "hl": None, "textId": ""},
        {"ts": 1721029226333.3333, "w": "de", "index": 459, "hl": None, "textId": ""},
        {
            "ts": 1721029226666.6667,
            "w": "c\x9cur",
            "index": 460,
            "hl": None,
            "textId": "",
        },
        {"ts": 1721029227000, "w": "en", "index": 461, "hl": None, "textId": ""},
        {
            "ts": 1721029227333.3333,
            "w": "appelant",
            "index": 462,
            "hl": None,
            "textId": "",
        },
        {"ts": 1721029227666.6667, "w": "le", "index": 463, "hl": None, "textId": ""},
        {"ts": 1721029228000, "w": "zéro", "index": 464, "hl": None, "textId": ""},
        {"ts": 1721029228333.3333, "w": "805", "index": 465, "hl": None, "textId": ""},
        {"ts": 1721029228666.6667, "w": "21", "index": 466, "hl": None, "textId": ""},
        {"ts": 1721029229000, "w": "30", "index": 467, "hl": None, "textId": ""},
        {"ts": 1721029230000, "w": "30", "index": 468, "hl": None, "textId": ""},
        {"ts": 1721029230333.3333, "w": "ou", "index": 469, "hl": None, "textId": ""},
        {"ts": 1721029230666.6667, "w": "en", "index": 470, "hl": None, "textId": ""},
        {"ts": 1721029231000, "w": "tapant", "index": 471, "hl": None, "textId": ""},
        {"ts": 1721029231250, "w": "maitre", "index": 472, "hl": None, "textId": ""},
        {"ts": 1721029231500, "w": "de", "index": 473, "hl": None, "textId": ""},
        {"ts": 1721029231750, "w": "c\x9cur", "index": 474, "hl": None, "textId": ""},
        {"ts": 1721029232000, "w": "sur", "index": 475, "hl": None, "textId": ""},
        {
            "ts": 1721029232333.3333,
            "w": "internet",
            "index": 476,
            "hl": None,
            "textId": "",
        },
        {"ts": 1721029232666.6667, "w": "et", "index": 477, "hl": None, "textId": ""},
        {"ts": 1721029233000, "w": "recevez", "index": 478, "hl": None, "textId": ""},
        {"ts": 1721029233250, "w": "votre", "index": 479, "hl": None, "textId": ""},
        {"ts": 1721029233500, "w": "porte", "index": 480, "hl": None, "textId": ""},
        {"ts": 1721029233750, "w": "clefs", "index": 481, "hl": None, "textId": ""},
        {"ts": 1721029234000, "w": "Maîtres", "index": 482, "hl": None, "textId": ""},
        {"ts": 1721029235666.6667, "w": "de", "index": 483, "hl": None, "textId": ""},
        {
            "ts": 1721029237333.3333,
            "w": "c\x9cur.",
            "index": 484,
            "hl": None,
            "textId": "",
        },
        {"ts": 1721029239000, "w": "Vous", "index": 485, "hl": None, "textId": ""},
        {"ts": 1721029239500, "w": "souhaitez", "index": 486, "hl": None, "textId": ""},
        {"ts": 1721029240000, "w": "devenir", "index": 487, "hl": None, "textId": ""},
        {
            "ts": 1721029240500,
            "w": "naturopathe",
            "index": 488,
            "hl": None,
            "textId": "",
        },
        {"ts": 1721029241000, "w": "et", "index": 489, "hl": None, "textId": ""},
        {"ts": 1721029241250, "w": "en", "index": 490, "hl": None, "textId": ""},
        {"ts": 1721029241500, "w": "faire", "index": 491, "hl": None, "textId": ""},
        {"ts": 1721029241750, "w": "votre", "index": 492, "hl": None, "textId": ""},
        {"ts": 1721029242000, "w": "métier,", "index": 493, "hl": None, "textId": ""},
        {
            "ts": 1721029242333.3333,
            "w": "alors",
            "index": 494,
            "hl": None,
            "textId": "",
        },
        {
            "ts": 1721029242666.6667,
            "w": "formez",
            "index": 495,
            "hl": None,
            "textId": "",
        },
        {"ts": 1721029243000, "w": "vous", "index": 496, "hl": None, "textId": ""},
        {"ts": 1721029243333.3333, "w": "dès", "index": 497, "hl": None, "textId": ""},
        {
            "ts": 1721029243666.6667,
            "w": "aujourd'hui,",
            "index": 498,
            "hl": None,
            "textId": "",
        },
        {"ts": 1721029244000, "w": "à", "index": 499, "hl": None, "textId": ""},
        {"ts": 1721029244250, "w": "votre", "index": 500, "hl": None, "textId": ""},
        {"ts": 1721029244500, "w": "rythme,", "index": 501, "hl": None, "textId": ""},
        {"ts": 1721029244750, "w": "depuis", "index": 502, "hl": None, "textId": ""},
        {"ts": 1721029245000, "w": "chez", "index": 503, "hl": None, "textId": ""},
        {"ts": 1721029245200, "w": "vous,", "index": 504, "hl": None, "textId": ""},
        {"ts": 1721029245400, "w": "avec", "index": 505, "hl": None, "textId": ""},
        {"ts": 1721029245600, "w": "le", "index": 506, "hl": None, "textId": ""},
        {"ts": 1721029245800, "w": "Centre", "index": 507, "hl": None, "textId": ""},
        {"ts": 1721029246000, "w": "européen", "index": 508, "hl": None, "textId": ""},
        {"ts": 1721029246333.3333, "w": "de", "index": 509, "hl": None, "textId": ""},
        {
            "ts": 1721029246666.6667,
            "w": "formation,",
            "index": 510,
            "hl": None,
            "textId": "",
        },
        {"ts": 1721029247000, "w": "cette", "index": 511, "hl": None, "textId": ""},
        {"ts": 1721029247500, "w": "formation", "index": 512, "hl": None, "textId": ""},
        {"ts": 1721029248000, "w": "ultra", "index": 513, "hl": None, "textId": ""},
        {"ts": 1721029248500, "w": "complète", "index": 514, "hl": None, "textId": ""},
        {"ts": 1721029249000, "w": "de", "index": 515, "hl": None, "textId": ""},
        {"ts": 1721029249333.3333, "w": "500", "index": 516, "hl": None, "textId": ""},
        {
            "ts": 1721029249666.6667,
            "w": "heures",
            "index": 517,
            "hl": None,
            "textId": "",
        },
        {"ts": 1721029250000, "w": "fera", "index": 518, "hl": None, "textId": ""},
        {"ts": 1721029250200, "w": "de", "index": 519, "hl": None, "textId": ""},
        {"ts": 1721029250400, "w": "vous", "index": 520, "hl": None, "textId": ""},
        {"ts": 1721029250600, "w": "une", "index": 521, "hl": None, "textId": ""},
        {
            "ts": 1721029250800,
            "w": "professionnelle",
            "index": 522,
            "hl": None,
            "textId": "",
        },
        {"ts": 1721029251000, "w": "de", "index": 523, "hl": None, "textId": ""},
        {"ts": 1721029251333.3333, "w": "la", "index": 524, "hl": None, "textId": ""},
        {
            "ts": 1721029251666.6667,
            "w": "naturopathie.",
            "index": 525,
            "hl": None,
            "textId": "",
        },
        {"ts": 1721029252000, "w": "Réaliser", "index": 526, "hl": None, "textId": ""},
        {"ts": 1721029253000, "w": "un", "index": 527, "hl": None, "textId": ""},
        {"ts": 1721029253250, "w": "bilan", "index": 528, "hl": None, "textId": ""},
        {"ts": 1721029253500, "w": "de", "index": 529, "hl": None, "textId": ""},
        {"ts": 1721029253750, "w": "vitalité", "index": 530, "hl": None, "textId": ""},
        {"ts": 1721029254000, "w": "ou", "index": 531, "hl": None, "textId": ""},
        {"ts": 1721029254250, "w": "un", "index": 532, "hl": None, "textId": ""},
        {"ts": 1721029254500, "w": "protocole", "index": 533, "hl": None, "textId": ""},
        {
            "ts": 1721029254750,
            "w": "personnalisé",
            "index": 534,
            "hl": None,
            "textId": "",
        },
        {"ts": 1721029255000, "w": "n'auront", "index": 535, "hl": None, "textId": ""},
        {"ts": 1721029255500, "w": "plus", "index": 536, "hl": None, "textId": ""},
        {"ts": 1721029256000, "w": "aucun", "index": 537, "hl": None, "textId": ""},
        {
            "ts": 1721029256333.3333,
            "w": "secret",
            "index": 538,
            "hl": None,
            "textId": "",
        },
        {"ts": 1721029256666.6667, "w": "pour", "index": 539, "hl": None, "textId": ""},
        {"ts": 1721029257000, "w": "vous.", "index": 540, "hl": None, "textId": ""},
        {
            "ts": 1721029257333.3333,
            "w": "Découvrez",
            "index": 541,
            "hl": None,
            "textId": "",
        },
        {
            "ts": 1721029257666.6667,
            "w": "gratuitement.",
            "index": 542,
            "hl": None,
            "textId": "",
        },
        {"ts": 1721029258000, "w": "Oui,", "index": 543, "hl": None, "textId": ""},
        {"ts": 1721029258500, "w": "vous", "index": 544, "hl": None, "textId": ""},
        {"ts": 1721029259000, "w": "avez", "index": 545, "hl": None, "textId": ""},
        {"ts": 1721029259250, "w": "bien", "index": 546, "hl": None, "textId": ""},
        {"ts": 1721029259500, "w": "entendu", "index": 547, "hl": None, "textId": ""},
        {"ts": 1721029259750, "w": "grâce.", "index": 548, "hl": None, "textId": ""},
        {
            "ts": 1721029260000,
            "w": "Gratuitement",
            "index": 549,
            "hl": None,
            "textId": "",
        },
        {"ts": 1721029260500, "w": "notre", "index": 550, "hl": None, "textId": ""},
        {"ts": 1721029261000, "w": "premier", "index": 551, "hl": None, "textId": ""},
        {"ts": 1721029261250, "w": "cours", "index": 552, "hl": None, "textId": ""},
        {"ts": 1721029261500, "w": "sur", "index": 553, "hl": None, "textId": ""},
        {"ts": 1721029261750, "w": "la", "index": 554, "hl": None, "textId": ""},
        {
            "ts": 1721029262000,
            "w": "phytothérapie",
            "index": 555,
            "hl": None,
            "textId": "",
        },
        {"ts": 1721029262333.3333, "w": "et", "index": 556, "hl": None, "textId": ""},
        {
            "ts": 1721029262666.6667,
            "w": "c'est",
            "index": 557,
            "hl": None,
            "textId": "",
        },
        {"ts": 1721029263000, "w": "sans", "index": 558, "hl": None, "textId": ""},
        {
            "ts": 1721029263333.3333,
            "w": "engagement.",
            "index": 559,
            "hl": None,
            "textId": "",
        },
        {
            "ts": 1721029263666.6667,
            "w": "Rendez",
            "index": 560,
            "hl": None,
            "textId": "",
        },
        {"ts": 1721029264000, "w": "vous", "index": 561, "hl": None, "textId": ""},
        {
            "ts": 1721029264333.3333,
            "w": "maintenant",
            "index": 562,
            "hl": None,
            "textId": "",
        },
        {"ts": 1721029264666.6667, "w": "sur", "index": 563, "hl": None, "textId": ""},
        {"ts": 1721029265000, "w": "Centre", "index": 564, "hl": None, "textId": ""},
        {"ts": 1721029265500, "w": "européen", "index": 565, "hl": None, "textId": ""},
        {"ts": 1721029266000, "w": "de", "index": 566, "hl": None, "textId": ""},
        {"ts": 1721029266500, "w": "formation", "index": 567, "hl": None, "textId": ""},
        {"ts": 1721029267000, "w": "Centre", "index": 568, "hl": None, "textId": ""},
        {"ts": 1721029268000, "w": "européen", "index": 569, "hl": None, "textId": ""},
        {
            "ts": 1721029268500,
            "w": "d'informations",
            "index": 570,
            "hl": None,
            "textId": "",
        },
        {"ts": 1721029269000, "w": "pour", "index": 571, "hl": None, "textId": ""},
        {"ts": 1721029271333.3333, "w": "y", "index": 572, "hl": None, "textId": ""},
        {
            "ts": 1721029273666.6667,
            "w": "faire.",
            "index": 573,
            "hl": None,
            "textId": "",
        },
        {"ts": 1721029276000, "w": "Ouais,", "index": 574, "hl": None, "textId": ""},
        {"ts": 1721029276500, "w": "facile.", "index": 575, "hl": None, "textId": ""},
        {"ts": 1721029277000, "w": "Depuis", "index": 576, "hl": None, "textId": ""},
        {"ts": 1721029278000, "w": "que", "index": 577, "hl": None, "textId": ""},
        {"ts": 1721029279000, "w": "son", "index": 578, "hl": None, "textId": ""},
        {"ts": 1721029279200, "w": "assurance", "index": 579, "hl": None, "textId": ""},
        {"ts": 1721029279400, "w": "auto", "index": 580, "hl": None, "textId": ""},
        {"ts": 1721029279600, "w": "est", "index": 581, "hl": None, "textId": ""},
        {"ts": 1721029279800, "w": "refait,", "index": 582, "hl": None, "textId": ""},
        {"ts": 1721029280000, "w": "tout", "index": 583, "hl": None, "textId": ""},
        {"ts": 1721029280500, "w": "lui", "index": 584, "hl": None, "textId": ""},
        {"ts": 1721029281000, "w": "paraît", "index": 585, "hl": None, "textId": ""},
        {"ts": 1721029281500, "w": "plus", "index": 586, "hl": None, "textId": ""},
        {"ts": 1721029282000, "w": "facile.", "index": 587, "hl": None, "textId": ""},
        {"ts": 1721029282500, "w": "Et", "index": 588, "hl": None, "textId": ""},
        {"ts": 1721029283000, "w": "voilà,", "index": 589, "hl": None, "textId": ""},
        {"ts": 1721029283250, "w": "tout", "index": 590, "hl": None, "textId": ""},
        {"ts": 1721029283500, "w": "est", "index": 591, "hl": None, "textId": ""},
        {"ts": 1721029283750, "w": "réglé.", "index": 592, "hl": None, "textId": ""},
        {"ts": 1721029284000, "w": "Un", "index": 593, "hl": None, "textId": ""},
        {"ts": 1721029284500, "w": "refill", "index": 594, "hl": None, "textId": ""},
        {
            "ts": 1721029285000,
            "w": "l'assurance.",
            "index": 595,
            "hl": None,
            "textId": "",
        },
        {"ts": 1721029286000, "w": "C'est", "index": 596, "hl": None, "textId": ""},
        {"ts": 1721029286500, "w": "facile", "index": 597, "hl": None, "textId": ""},
        {"ts": 1721029287000, "w": "à", "index": 598, "hl": None, "textId": ""},
        {
            "ts": 1721029287333.3333,
            "w": "vivre",
            "index": 599,
            "hl": None,
            "textId": "",
        },
        {"ts": 1721029287666.6667, "w": "en", "index": 600, "hl": None, "textId": ""},
        {"ts": 1721029288000, "w": "ce", "index": 601, "hl": None, "textId": ""},
        {"ts": 1721029288200, "w": "moment.", "index": 602, "hl": None, "textId": ""},
    ]


@pytest.fixture
def test_predict_keyword_fr() -> str:
    """Predict keyword fixture for French transcript."""
    return ["CENTRE EUROPEEN DE FORMATION"]


@pytest.fixture
def test_expected_predict_output_fr() -> List[str]:
    """Expected predict output fixture for French transcript."""
    return PredictResponseSchema.from_data(
        version=1,
        namespace="transcript-segmentation",
        attributes={
            "start_time": 1721029232000.0,
            "end_time": 1721029278666.6667,
            "transcript_start_time": 1721029239000,
            "transcript_end_time": 1721029273666.6667,
            "title": "example title",
            "summary": "example summary",
            "segment": "example segment",
            "ad": True,
        },
    )


@pytest.fixture
def test_predict_input() -> str:
    """Predict input fixture."""
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
        {"ts": 1701127859428.5715, "w": "ChatGPT-4.", "index": 108},
        {"ts": 1701127859428.9715, "w": "GPT-4", "index": 109},
        {"ts": 1701127859728.9715, "w": "supports", "index": 110},
        {"ts": 1701127859928.9715, "w": "Covered", "index": 111},
        {"ts": 1701127860428.9715, "w": "California", "index": 112},
        {"ts": 1701127860828.9715, "w": "to", "index": 113},
        {"ts": 1701127861428.9715, "w": "provide", "index": 114},
        {"ts": 1701127861828.9715, "w": "free", "index": 115},
        {"ts": 1701127862428.9715, "w": "service", "index": 116},
        {"ts": 1701127862828.9715, "w": "from", "index": 117},
        {"ts": 1701127863228.9715, "w": "the", "index": 118},
        {"ts": 1701127863828.9715, "w": "state", "index": 119},
        {"ts": 1701127864228.9715, "w": "that's", "index": 120},
        {"ts": 1701127864628.9715, "w": "already", "index": 121},
        {"ts": 1701127865028.9715, "w": "helped", "index": 122},
        {"ts": 1701127865428.9715, "w": "millions", "index": 123},
        {"ts": 1701127865828.9715, "w": "of", "index": 124},
        {"ts": 1701127866228.9715, "w": "people", "index": 125},
        {"ts": 1701127870228.9715, "w": "by", "index": 126},
        {"ts": 1701127874228.9715, "w": "AI", "index": 127},
        {"ts": 1701127878228.9715, "w": "to", "index": 128},
        {"ts": 1701127882228.9715, "w": "help", "index": 129},
        {"ts": 1701127886228.9715, "w": "pay", "index": 130},
        {"ts": 1701127890228.9715, "w": "for", "index": 131},
        {"ts": 1701127894228.9715, "w": "health", "index": 132},
        {"ts": 1701127898228.9715, "w": "insurance.", "index": 133},
    ]  # noqa: E501


@pytest.fixture
def test_predict_keyword() -> str:
    """Predict keyword fixture."""
    return ["Ai"]


@pytest.fixture
def test_inference_params() -> str:
    """Predict parameter fixture."""
    return {
        "country": "FRA",
        "channel": "channel",
        "query": "sample query",
        "offset_start_buffer": -7000.0,
        "offset_end_buffer": 5000.0,
    }


@pytest.fixture
def test_expected_predict_output() -> List[str]:
    """Expected predict output fixture."""
    return PredictResponseSchema.from_data(
        version=1,
        namespace="transcript-segmentation",
        attributes={
            "start_time": 1701127816000.0,
            "end_time": 1701127859428.5715,
            "transcript_start_time": 1701127820000.0,
            "transcript_end_time": 1701127859428.5715,
            "title": "example title",
            "summary": "example summary",
            "segment": "example segment",
            "ad": True,
        },
    )


@pytest.fixture
def test_expected_bio_output():
    """Test expected bio output."""
    return BioResponseSchema.from_data(
        version=1,
        namespace="transcript-segmentation",
        attributes={"model_name": "transcript-segmentation"},
    )
