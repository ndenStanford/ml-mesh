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
    root_response = requests.get("http://serve:8000/gch-summarization/v1/")

    assert root_response.status_code == 200


def test_model_server_bio():
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    readiness_response = requests.get("http://serve:8000/gch-summarization/v1/bio")

    assert readiness_response.status_code == 200
    assert (
        readiness_response.model_dump_json()["data"]["attributes"].get("model_card")
        is not None
    )


def test_model_server_liveness():
    """Tests the liveness endpoint of a ModelServer (not running) instance."""
    liveness_response = requests.get("http://serve:8000/gch-summarization/v1/live")

    assert liveness_response.status_code == 200
    assert liveness_response.model_dump_json() == LivenessProbeResponse().model_dump()


def test_model_server_readiness():
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    readiness_response = requests.get("http://serve:8000/gch-summarization/v1/ready")

    assert readiness_response.status_code == 200
    assert readiness_response.model_dump_json() == ReadinessProbeResponse().model_dump()


@pytest.mark.parametrize(
    "payload, expected_response",
    [
        (
            {
                "data": {
                    "namespace": "gch-summarization",
                    "attributes": {
                        "content": "Sky News announces slate of special programming for the appointment of the UK's new \
Prime Minister.\nSky News' political programming will expand ahead of a momentous week \
in UK politics with the impending announcement of the new Prime Minister. Sky News' key \
political programmes will return to bring audiences in-depth discussion and analysis of \
all the latest news with live coverage from Downing Street and Westminster.\nHead of Sky \
News, John Ryley:\n'This is a momentous week in British politics, where a new Prime Minister \
will take on an in-tray bursting with crunch decisions.",
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
                    "namespace": "gch-summarization",
                    "attributes": {
                        "summary": "Sky News to expand political programming ahead of the appointment of the new Prime \
Minister. Key political programmes will return to bring audiences in-depth discussion and analysis."
                    },
                },
            },
        )
    ],
)
def test_model_server_prediction(payload, expected_response):
    """Tests predict endpoint of the gch summarization ModelServer."""
    response = requests.post(
        "http://serve:8000/gch-summarization/v1/predict",
        json=payload,
    )

    assert response.status_code == 200
    # TODO: assert score close to expected
    assert response.model_dump_json() == expected_response


@pytest.mark.parametrize(
    "payload",
    [
        (
            {
                "data": {
                    "namespace": "gch-summarization",
                    "attributes": {
                        "content": "天空新闻宣布了英国新任总理任命的一系列特别节目总理。\
                        天空新闻的政治节目将在重要的一周之前扩大英国政坛即将宣布新首相。\
                        天空新闻键时政类节目将回归，为观众带来深度讨论与剖析“ \
                        来自唐宁街和威斯敏斯特的所有最新新闻现场报道。\
                        天空电视台负责人新闻，约翰·莱利：“这是英国政坛重要的一周，\
                        新首相将处理一个充满紧急决策的托盘。"
                    },
                    "parameters": {
                        "language": "zh",
                    },
                }
            }
        )
    ],
)
def test_model_server_prediction_invalid_language(payload):
    """Tests predict endpoint of the gch summarization ModelServer."""
    response = requests.post(
        "http://serve:8000/gch-summarization/v1/predict",
        json=payload,
    )

    assert response.status_code == 204
