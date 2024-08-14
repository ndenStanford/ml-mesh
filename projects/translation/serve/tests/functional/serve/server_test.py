"""Server functional tests."""

# 3rd party libraries
import pytest
import requests

# Internal libraries
from onclusiveml.serving.rest.serve import (
    LivenessProbeResponse,
    ReadinessProbeResponse,
)


def test_model_server_liveness():
    """Tests the liveness endpoint of a ModelServer (not running) instance."""
    liveness_response = requests.get("http://serve:8001/translation/v1/live")

    assert liveness_response.status_code == 200
    assert liveness_response.json() == LivenessProbeResponse().model_dump()


def test_model_server_readiness():
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    readiness_response = requests.get("http://serve:8001/translation/v1/ready")

    assert readiness_response.status_code == 200
    assert readiness_response.json() == ReadinessProbeResponse().model_dump()


def test_model_server_bio():
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    readiness_response = requests.get("http://serve:8001/translation/v1/bio")

    assert readiness_response.status_code == 200
    assert readiness_response.json()["data"]["attributes"].get("model_name") is not None


@pytest.mark.parametrize(
    "payload, expected_response",
    [
        (
            {
                "data": {
                    "identifier": None,
                    "namespace": "translation",
                    "attributes": {
                        "content": "Tottenham Hotspur Football Club has drawn up plans for student flats on the site of a former printworks near its stadium.",  # noqa
                    },
                    "parameters": {
                        "target_language": "fr",
                        "translation": True,
                    },
                }
            },
            {
                "version": 1,
                "data": {
                    "identifier": None,
                    "namespace": "translation",
                    "attributes": {
                        "source_language": "en",
                        "target_language": "fr",
                        "translated_text": "Le Tottenham Hotspur Football Club a élaboré des plans pour des appartements étudiants sur le site d'une ancienne imprimerie à proximité de son stade.",  # noqa
                    },
                },
            },
        ),
        (
            {
                "data": {
                    "identifier": None,
                    "namespace": "translation",
                    "attributes": {
                        "content": "وبما أن هذا مجرد اختبار للكشف عن اللغة، فأنا أكتب كل ما يجول في خاطري، وأرجو أن يكون الأمر على ما يرام مع من سيتحقق منه لاحقاً.",  # noqa
                    },
                    "parameters": {
                        "translation": False,
                    },
                }
            },
            {
                "version": 1,
                "data": {
                    "identifier": None,
                    "namespace": "translation",
                    "attributes": {
                        "source_language": "ar",
                        "target_language": None,
                        "translated_text": None,  # noqa
                    },
                },
            },
        ),
        (
            {
                "data": {
                    "identifier": None,
                    "namespace": "translation",
                    "attributes": {
                        "content": "As this is just a test to detect the language, I am writing anything going through my mind, I hope it is fine with whoever will check it out later on.",  # noqa
                    },
                    "parameters": {
                        "translation": False,
                    },
                }
            },
            {
                "version": 1,
                "data": {
                    "identifier": None,
                    "namespace": "translation",
                    "attributes": {
                        "source_language": "en",
                        "target_language": None,
                        "translated_text": None,  # noqa
                    },
                },
            },
        ),
        (
            {
                "data": {
                    "identifier": None,
                    "namespace": "translation",
                    "attributes": {
                        "content": "これは言語を検出するためのテストであり、私の頭の中にあることを何でも書いているので、後で誰がチェックしても問題ないことを願っている。",  # noqa
                    },
                    "parameters": {
                        "translation": False,
                    },
                }
            },
            {
                "version": 1,
                "data": {
                    "identifier": None,
                    "namespace": "translation",
                    "attributes": {
                        "source_language": "ja",
                        "target_language": None,
                        "translated_text": None,
                    },
                },
            },
        ),
        (
            {
                "data": {
                    "identifier": None,
                    "namespace": "translation",
                    "attributes": {
                        "content": "これは言語を検出するためのテストであり、私の頭の中にあることを何でも書いているので、後で誰がチェックしても問題ないことを願っている。",  # noqa
                    },
                    "parameters": {
                        "source_language": "ja",
                        "target_language": "en",
                        "translation": True,
                    },
                }
            },
            {
                "version": 1,
                "data": {
                    "identifier": None,
                    "namespace": "translation",
                    "attributes": {
                        "source_language": "ja",
                        "target_language": "en",
                        "translated_text": "This is a test to detect language, and I'm writing whatever's in my head, so I hope it doesn't matter if anyone checks it later.",  # noqa
                    },
                },
            },
        ),
        (
            {
                "data": {
                    "identifier": None,
                    "namespace": "translation",
                    "attributes": {
                        "content": "This is a test to detect language, and I'm writing whatever's in my head, so I hope it doesn't matter if anyone checks it later.",  # noqa
                    },
                    "parameters": {
                        "target_language": "ja",
                        "translation": True,
                    },
                }
            },
            {
                "version": 1,
                "data": {
                    "identifier": None,
                    "namespace": "translation",
                    "attributes": {
                        "source_language": "en",
                        "target_language": "ja",
                        "translated_text": "これは言語を検出するためのテストで、頭の中にあることは何でも書いているので、後で誰かがチェックしても問題にならないことを願っています。",  # noqa
                    },
                },
            },
        ),
        (
            {
                "data": {
                    "identifier": None,
                    "namespace": "translation",
                    "attributes": {
                        "content": "由于这只是一个检测语言的测试，我写的都是自己的想法，希望以后谁来检查都没问题。",  # noqa
                    },
                    "parameters": {
                        "translation": False,
                    },
                }
            },
            {
                "version": 1,
                "data": {
                    "identifier": None,
                    "namespace": "translation",
                    "attributes": {
                        "source_language": "Language not found",
                        "target_language": None,
                        "translated_text": None,  # noqa
                    },
                },
            },
        ),
    ],
)
def test_model_server_prediction(test_client, payload, expected_response):
    """Tests the predict endpoint of a running ModelServer instance."""
    response = test_client.post(
        "/translation/v1/predict",
        json=payload,
    )
    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.parametrize(
    "payload,expected_error_detail",
    [
        (
            {
                "data": {
                    "identifier": None,
                    "namespace": "translation",
                    "attributes": {
                        "content": "Irrelevant message as we want to test the language detection.",  # noqa
                    },
                    "parameters": {
                        "source_language": "invalid language",
                        "target_language": "fr",
                        "translation": True,
                    },
                }
            },
            "The language reference 'invalid language' could not be mapped, or the language could not be inferred from the content.",  # noqa: E501
        ),
    ],
)
def test_model_server_prediction_invalid_language(
    test_client, payload, expected_error_detail
):
    """Tests the language validation of the predict endpoint of a running ModelServer instance."""
    response = test_client.post(
        "/translation/v1/predict",
        json=payload,
    )

    assert response.status_code == 204
    assert response.text == ""
