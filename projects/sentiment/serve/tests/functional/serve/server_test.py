"""Server functional tests."""

# 3rd party libraries
import pytest
import requests

# Internal libraries
from onclusiveml.serving.rest.serve import (
    LivenessProbeResponse,
    ReadinessProbeResponse,
)


def test_model_server_root():
    """Tests the root endpoint of a ModelServer (not running) instance."""
    root_response = requests.get("http://serve:8000/sentiment/v1/")

    assert root_response.status_code == 200


def test_model_server_liveness():
    """Tests the liveness endpoint of a ModelServer (not running) instance."""
    liveness_response = requests.get("http://serve:8000/sentiment/v1/live")

    assert liveness_response.status_code == 200
    assert liveness_response.json() == LivenessProbeResponse().dict()


def test_model_server_readiness():
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    readiness_response = requests.get("http://serve:8000/sentiment/v1/ready")

    assert readiness_response.status_code == 200
    assert readiness_response.json() == ReadinessProbeResponse().dict()


def test_model_server_bio():
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    readiness_response = requests.get("http://serve:8000/sentiment/v1/bio")

    assert readiness_response.status_code == 200
    assert readiness_response.json()["data"]["attributes"].get("model_card") is not None


@pytest.mark.parametrize(
    "payload, expected_response",
    [
        (
            {
                "data": {
                    "namespace": "sentiment",
                    "attributes": {
                        "content": "London is a wonderful city. John is a terrible man.",
                        "entities": [
                            {
                                "entity_type": "LOC",
                                "entity_text": "London",
                                "score": "0.99966383",
                                "sentence_index": 0,
                                "start": 0,
                                "end": 6,
                            },
                            {
                                "entity_type": "PER",
                                "entity_text": "John",
                                "score": "0.9991505",
                                "sentence_index": 1,
                                "start": 0,
                                "end": 4,
                            },
                        ],
                    },
                    "parameters": {
                        "language": "en",
                    },
                }
            },
            {
                "version": 1,
                "data": {
                    "identifier": None,
                    "namespace": "sentiment",
                    "attributes": {
                        "label": "positive",
                        "negative_prob": 0.4854,
                        "positive_prob": 0.4794,
                        "entities": [
                            {
                                "entity_type": "LOC",
                                "entity_text": "London",
                                "score": 0.99966383,
                                "sentence_index": 0,
                                "start": 0,
                                "end": 6,
                                "sentiment": "positive",
                            },
                            {
                                "entity_type": "PER",
                                "entity_text": "John",
                                "score": 0.9991505,
                                "sentence_index": 1,
                                "start": 0,
                                "end": 4,
                                "sentiment": "negative",
                            },
                        ],
                    },
                },
            },
        )
    ],
)
def test_model_server_prediction(payload, expected_response):
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    response = requests.post(
        "http://serve:8000/sentiment/v1/predict",
        json=payload,
    )

    assert response.status_code == 200
    # TODO: assert score close to expected
    assert response.json() == expected_response


@pytest.mark.parametrize(
    "payload, expected_response",
    [
        (
            {
                "data": {
                    "namespace": "sentiment",
                    "attributes": {"content": "AI is a fantastic tool."},
                    "parameters": {"language": "en"},
                }
            },
            {
                "version": 1,
                "data": {
                    "identifier": None,
                    "namespace": "sentiment",
                    "attributes": {
                        "label": "positive",
                        "negative_prob": 0.0256,
                        "positive_prob": 0.9139,
                        "entities": None,
                    },
                },
            },
        )
    ],
)
def test_model_server_prediction_no_entities(payload, expected_response):
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    response = requests.post(
        "http://serve:8000/sentiment/v1/predict",
        json=payload,
    )

    assert response.status_code == 200
    # TODO: assert score close to expected
    assert response.json() == expected_response


@pytest.mark.parametrize(
    "payload, expected_response",
    [
        # Test case for an unsupported language (invalid language code)
        (
            {
                "data": {
                    "namespace": "sentiment",
                    "attributes": {
                        "content": "Esta es una prueba con un idioma no soportado.",
                        "entities": [],
                    },
                    "parameters": {
                        "language": "xyz",
                    },
                }
            },
            {
                "status": 422,
                "detail": (
                    "The language reference 'xyz' could not be mapped, or the language "
                    "could not be inferred from the content. Supported references are: "
                    "['ar', 'hy', 'eu', 'bn', 'my', 'ca', 'zh', 'hr', "
                    "'cs', 'da', 'nl', 'en', 'et', "
                    "'fi', 'fr', 'de', 'el', 'gu', 'he', 'hi', 'hu', 'id', 'it', 'ja', 'kn', 'kk', "
                    "'ko', 'ku', 'lv', 'lt', 'mk', 'ms', 'ml', 'mr', 'ne', 'no', 'pa', 'pl', 'pt', "
                    "'ro', 'ru', 'sa', 'sk', 'sl', 'es', 'sv', 'ta', 'te', 'th', 'tr', 'uk', 'ur', "
                    "'uz', 'vi', 'cy']. Supported languages are: [<LanguageIso.AR: 'ar'>, "
                    "<LanguageIso.HY: 'hy'>, <LanguageIso.EU: 'eu'>, <LanguageIso.BN: 'bn'>, "
                    "<LanguageIso.MY: 'my'>, <LanguageIso.CA: 'ca'>, <LanguageIso.ZH: 'zh'>, "
                    "<LanguageIso.HR: 'hr'>, <LanguageIso.CS: 'cs'>, <LanguageIso.DA: 'da'>, "
                    "<LanguageIso.NL: 'nl'>, <LanguageIso.EN: 'en'>, <LanguageIso.ET: 'et'>, "
                    "<LanguageIso.FI: 'fi'>, <LanguageIso.FR: 'fr'>, <LanguageIso.DE: 'de'>, "
                    "<LanguageIso.EL: 'el'>, <LanguageIso.GU: 'gu'>, <LanguageIso.HE: 'he'>, "
                    "<LanguageIso.HI: 'hi'>, <LanguageIso.HU: 'hu'>, <LanguageIso.ID: 'id'>, "
                    "<LanguageIso.IT: 'it'>, <LanguageIso.JA: 'ja'>, <LanguageIso.KN: 'kn'>, "
                    "<LanguageIso.KK: 'kk'>, <LanguageIso.KO: 'ko'>, <LanguageIso.KU: 'ku'>, "
                    "<LanguageIso.LV: 'lv'>, <LanguageIso.LT: 'lt'>, <LanguageIso.MK: 'mk'>, "
                    "<LanguageIso.MS: 'ms'>, <LanguageIso.ML: 'ml'>, <LanguageIso.MR: 'mr'>, "
                    "<LanguageIso.NE: 'ne'>, <LanguageIso.NO: 'no'>, <LanguageIso.PA: 'pa'>, "
                    "<LanguageIso.PL: 'pl'>, <LanguageIso.PT: 'pt'>, <LanguageIso.RO: 'ro'>, "
                    "<LanguageIso.RU: 'ru'>, <LanguageIso.SA: 'sa'>, <LanguageIso.SK: 'sk'>, "
                    "<LanguageIso.SL: 'sl'>, <LanguageIso.ES: 'es'>, <LanguageIso.SV: 'sv'>, "
                    "<LanguageIso.TA: 'ta'>, <LanguageIso.TE: 'te'>, <LanguageIso.TH: 'th'>, "
                    "<LanguageIso.TR: 'tr'>, <LanguageIso.UK: 'uk'>, <LanguageIso.UR: 'ur'>, "
                    "<LanguageIso.UZ: 'uz'>, <LanguageIso.VI: 'vi'>, <LanguageIso.CY: 'cy'>]."
                ),
            },
        ),
        # Test case for a correct but unsupported language code
        (
            {
                "data": {
                    "namespace": "sentiment",
                    "attributes": {
                        "content": "Ĉi tiu estas testo en ne subtenata lingvo.",
                        "entities": [],
                    },
                    "parameters": {
                        "language": "eo",
                    },
                }
            },
            {
                "status": 422,
                "detail": (
                    "The language reference 'eo' could not be mapped, or the language could not be "
                    "inferred from the content. Supported references are: ['ar', 'hy', 'eu', 'bn', "
                    "'my', 'ca', 'zh', 'hr', 'cs', 'da', 'nl', 'en', 'et', 'fi', 'fr', 'de', 'el', "
                    "'gu', 'he', 'hi', 'hu', 'id', 'it', 'ja', 'kn', 'kk', 'ko', 'ku', 'lv', 'lt', "
                    "'mk', 'ms', 'ml', 'mr', 'ne', 'no', 'pa', 'pl', 'pt', 'ro', 'ru', 'sa', 'sk', "
                    "'sl', 'es', 'sv', 'ta', 'te', 'th', 'tr', 'uk', 'ur', 'uz', 'vi', 'cy']. "
                    "Supported languages are: [<LanguageIso.AR: 'ar'>, <LanguageIso.HY: 'hy'>, "
                    "<LanguageIso.EU: 'eu'>, <LanguageIso.BN: 'bn'>, <LanguageIso.MY: 'my'>, "
                    "<LanguageIso.CA: 'ca'>, <LanguageIso.ZH: 'zh'>, <LanguageIso.HR: 'hr'>, "
                    "<LanguageIso.CS: 'cs'>, <LanguageIso.DA: 'da'>, <LanguageIso.NL: 'nl'>, "
                    "<LanguageIso.EN: 'en'>, <LanguageIso.ET: 'et'>, <LanguageIso.FI: 'fi'>, "
                    "<LanguageIso.FR: 'fr'>, <LanguageIso.DE: 'de'>, <LanguageIso.EL: 'el'>, "
                    "<LanguageIso.GU: 'gu'>, <LanguageIso.HE: 'he'>, <LanguageIso.HI: 'hi'>, "
                    "<LanguageIso.HU: 'hu'>, <LanguageIso.ID: 'id'>, <LanguageIso.IT: 'it'>, "
                    "<LanguageIso.JA: 'ja'>, <LanguageIso.KN: 'kn'>, <LanguageIso.KK: 'kk'>, "
                    "<LanguageIso.KO: 'ko'>, <LanguageIso.KU: 'ku'>, <LanguageIso.LV: 'lv'>, "
                    "<LanguageIso.LT: 'lt'>, <LanguageIso.MK: 'mk'>, <LanguageIso.MS: 'ms'>, "
                    "<LanguageIso.ML: 'ml'>, <LanguageIso.MR: 'mr'>, <LanguageIso.NE: 'ne'>, "
                    "<LanguageIso.NO: 'no'>, <LanguageIso.PA: 'pa'>, <LanguageIso.PL: 'pl'>, "
                    "<LanguageIso.PT: 'pt'>, <LanguageIso.RO: 'ro'>, <LanguageIso.RU: 'ru'>, "
                    "<LanguageIso.SA: 'sa'>, <LanguageIso.SK: 'sk'>, <LanguageIso.SL: 'sl'>, "
                    "<LanguageIso.ES: 'es'>, <LanguageIso.SV: 'sv'>, <LanguageIso.TA: 'ta'>, "
                    "<LanguageIso.TE: 'te'>, <LanguageIso.TH: 'th'>, <LanguageIso.TR: 'tr'>, "
                    "<LanguageIso.UK: 'uk'>, <LanguageIso.UR: 'ur'>, <LanguageIso.UZ: 'uz'>, "
                    "<LanguageIso.VI: 'vi'>, <LanguageIso.CY: 'cy'>]."
                ),
            },
        ),
        # Test case for Chinese
        (
            {
                "data": {
                    "namespace": "sentiment",
                    "attributes": {
                        "content": "北京是中国的首都。",
                        "entities": [
                            {
                                "entity_type": "LOC",
                                "entity_text": "北京",
                                "score": "0.9999",
                                "sentence_index": 0,
                                "start": 0,
                                "end": 2,
                            },
                        ],
                    },
                    "parameters": {
                        "language": "zh",
                    },
                }
            },
            {
                "version": 1,
                "data": {
                    "identifier": None,
                    "attributes": {
                        "entities": [
                            {
                                "end": 2,
                                "entity_text": "北京",
                                "entity_type": "LOC",
                                "score": 0.9999,
                                "sentence_index": 0,
                                "sentiment": "positive",
                                "start": 0,
                            }
                        ],
                        "label": "positive",
                        "negative_prob": 0.1478,
                        "positive_prob": 0.3239,
                    },
                    "namespace": "sentiment",
                },
            },
        ),
    ],
)
def test_new_language_cases(payload, expected_response):
    """Tests the sentiment prediction endpoint for new language scenarios."""
    response = requests.post(
        "http://serve:8000/sentiment/v1/predict",
        json=payload,
    )

    if response.status_code != 200:
        assert response.status_code == expected_response.get("status", 500)
        assert response.json().get("detail") == expected_response["detail"]
    else:
        assert response.status_code == 200
        assert response.json() == expected_response
