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
    liveness_response = requests.get("http://serve:8000/ner/v1/live")

    assert liveness_response.status_code == 200
    assert liveness_response.json() == LivenessProbeResponse().model_dump()


def test_model_server_readiness():
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    readiness_response = requests.get("http://serve:8000/ner/v1/ready")

    assert readiness_response.status_code == 200
    assert readiness_response.json() == ReadinessProbeResponse().model_dump()


def test_model_server_bio():
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    readiness_response = requests.get("http://serve:8000/ner/v1/bio")

    assert readiness_response.status_code == 200
    assert readiness_response.json()["data"]["attributes"].get("model_card") is not None


@pytest.mark.parametrize(
    "payload, expected_response",
    [
        # Test case for English (no entity)
        (
            {
                "data": {
                    "identifier": None,
                    "namespace": "ner",
                    "attributes": {
                        "content": "House prices were unchanged last month, defying predictions of another drop, but they are unlikely to have troughed just yet."  # noqa
                    },
                    "parameters": {"language": "en"},
                }
            },
            {
                "version": 1,
                "data": {
                    "identifier": None,
                    "namespace": "ner",
                    "attributes": {"entities": []},
                },
            },
        ),
        # Test case for English (with entities)
        (
            {
                "data": {
                    "identifier": None,
                    "namespace": "ner",
                    "attributes": {
                        "content": "Amazon steps up AI race with up to 4 billion deal to invest in Anthropic."  # noqa
                    },
                    "parameters": {"language": "en"},
                }
            },
            {
                "version": 1,
                "data": {
                    "identifier": None,
                    "namespace": "ner",
                    "attributes": {
                        "entities": [
                            {
                                "entity_type": "ORG",
                                "entity_text": "Amazon",
                                "score": 0.9989171028137207,
                                "sentence_index": 0,
                                "start": 0,
                                "end": 6,
                            }
                        ]
                    },
                },
            },
        ),
        # Test case for Japanese (with entities)
        (
            {
                "data": {
                    "identifier": None,
                    "namespace": "ner",
                    "attributes": {
                        "content": "エアビーアンドビーは、2008年に設立されたオンライン宿泊シェアプラットフォームです。日本でエアビーアンドビーを利用する際、ホストは宿泊者の名前、住所、職業、滞在期間などの情報を記録する必要があります。外国人宿泊者の場合、パスポート番号と国籍も記録が必要です。"  # noqa
                    },
                    "parameters": {"language": "ja"},
                }
            },
            {
                "version": 1,
                "data": {
                    "identifier": None,
                    "namespace": "ner",
                    "attributes": {
                        "entities": [
                            {
                                "entity_type": "ORG",
                                "entity_text": "エアビーアンドビー",
                                "score": 0.9992916285991669,
                                "sentence_index": 0,
                                "start": 0,
                                "end": 9,
                            },
                            {
                                "entity_type": "LOC",
                                "entity_text": "日本で",
                                "score": 0.8986428380012512,
                                "sentence_index": 1,
                                "start": 0,
                                "end": 3,
                            },
                            {
                                "entity_type": "ORG",
                                "entity_text": "エアビーアンドビー",
                                "score": 0.9988850255807241,
                                "sentence_index": 1,
                                "start": 3,
                                "end": 12,
                            },
                        ]
                    },
                },
            },
        ),
        # Test case for Korean Airbnb (with entities)
        (
            {
                "data": {
                    "identifier": None,
                    "namespace": "ner",
                    "attributes": {
                        "content": "에어비앤비는 2008년에 설립된 온라인 숙박 공유 플랫폼입니다. 한국에서 에어비앤비를 이용할 때는 호스트가 모든 투숙객의 이름, 주소, 직업, 체류 기간 등의 정보를 기록해야 합니다. 외국인 투숙객의 경우 여권 번호와 국적도 기록해야 합니다."  # noqa
                    },
                    "parameters": {"language": "ko"},
                }
            },
            {
                "version": 1,
                "data": {
                    "identifier": None,
                    "namespace": "ner",
                    "attributes": {
                        "entities": [
                            {
                                "entity_type": "ORG",
                                "entity_text": "에어비앤비",
                                "score": 0.9997547745704651,
                                "sentence_index": 0,
                                "start": 0,
                                "end": 5,
                            },
                            {
                                "entity_type": "LOC",
                                "entity_text": "한국",
                                "score": 0.9992456436157227,
                                "sentence_index": 1,
                                "start": 0,
                                "end": 2,
                            },
                            {
                                "entity_type": "ORG",
                                "entity_text": "에어비앤비를",
                                "score": 0.9993805646896362,
                                "sentence_index": 1,
                                "start": 5,
                                "end": 11,
                            },
                        ]
                    },
                },
            },
        ),
        # Test case for English (multiple documents)
        (
            {
                "data": {
                    "identifier": None,
                    "namespace": "ner",
                    "attributes": {
                        "content": [
                            "The Eiffel Tower, located in Paris, France, was designed by Gustave Eiffel and completed in 1889. It has since become one of the most recognizable landmarks in the world, attracting millions of visitors annually.",
                            "In 2020, SpaceX, founded by Elon Musk, successfully launched astronauts to the International Space Station from American soil for the first time since the retirement of the Space Shuttle program in 2011.",
                            "William Shakespeare, the renowned English playwright, wrote 'Romeo and Juliet' in the late 16th century. The tragic love story, set in Verona, Italy, has been adapted countless times for stage and screen.",
                            "The Great Barrier Reef, stretching over 2,300 kilometers off the coast of Queensland, Australia, is the world's largest coral reef system. It is home to diverse marine life and visible from space.",
                            "Apple Inc., headquartered in Cupertino, California, revolutionized the smartphone industry with the introduction of the iPhone in 2007. The company's co-founder, Steve Jobs, played a crucial role in its development.",
                        ]  # noqa
                    },
                    "parameters": {"language": "en"},
                }
            },
            {
                "version": 1,
                "data": {
                    "identifier": None,
                    "namespace": "ner",
                    "attributes": {
                        "entities": [
                            [
                                {
                                    "entity_type": "LOC",
                                    "entity_text": "Eiffel Tower",
                                    "score": 0.9981139898300171,
                                    "sentence_index": 0,
                                    "start": 4,
                                    "end": 16,
                                },
                                {
                                    "entity_type": "LOC",
                                    "entity_text": "Paris",
                                    "score": 0.998245120048523,
                                    "sentence_index": 0,
                                    "start": 29,
                                    "end": 34,
                                },
                                {
                                    "entity_type": "LOC",
                                    "entity_text": "France",
                                    "score": 0.999722421169281,
                                    "sentence_index": 0,
                                    "start": 36,
                                    "end": 42,
                                },
                                {
                                    "entity_type": "PER",
                                    "entity_text": "Gustave Eiffel",
                                    "score": 0.9995022614796957,
                                    "sentence_index": 0,
                                    "start": 60,
                                    "end": 74,
                                },
                            ],
                            [
                                {
                                    "entity_type": "ORG",
                                    "entity_text": "SpaceX",
                                    "score": 0.9997899830341339,
                                    "sentence_index": 0,
                                    "start": 9,
                                    "end": 15,
                                },
                                {
                                    "entity_type": "PER",
                                    "entity_text": "Elon Musk",
                                    "score": 0.9996558427810669,
                                    "sentence_index": 0,
                                    "start": 28,
                                    "end": 37,
                                },
                                {
                                    "entity_type": "LOC",
                                    "entity_text": "International Space Station",
                                    "score": 0.9997769395510355,
                                    "sentence_index": 0,
                                    "start": 79,
                                    "end": 106,
                                },
                            ],
                            [
                                {
                                    "entity_type": "PER",
                                    "entity_text": "William Shakespeare",
                                    "score": 0.9998430907726288,
                                    "sentence_index": 0,
                                    "start": 0,
                                    "end": 19,
                                },
                                {
                                    "entity_type": "LOC",
                                    "entity_text": "Verona",
                                    "score": 0.9992495179176331,
                                    "sentence_index": 1,
                                    "start": 30,
                                    "end": 36,
                                },
                                {
                                    "entity_type": "LOC",
                                    "entity_text": "Italy",
                                    "score": 0.9998304843902588,
                                    "sentence_index": 1,
                                    "start": 38,
                                    "end": 43,
                                },
                            ],
                            [
                                {
                                    "entity_type": "LOC",
                                    "entity_text": "Great Barrier Reef",
                                    "score": 0.9997691154479981,
                                    "sentence_index": 0,
                                    "start": 4,
                                    "end": 22,
                                },
                                {
                                    "entity_type": "LOC",
                                    "entity_text": "Queensland",
                                    "score": 0.9995834231376648,
                                    "sentence_index": 0,
                                    "start": 74,
                                    "end": 84,
                                },
                                {
                                    "entity_type": "LOC",
                                    "entity_text": "Australia",
                                    "score": 0.9997743964195251,
                                    "sentence_index": 0,
                                    "start": 86,
                                    "end": 95,
                                },
                            ],
                            [
                                {
                                    "entity_type": "ORG",
                                    "entity_text": "Apple Inc.",
                                    "score": 0.9988864461580912,
                                    "sentence_index": 0,
                                    "start": 0,
                                    "end": 10,
                                },
                                {
                                    "entity_type": "LOC",
                                    "entity_text": "Cupertino",
                                    "score": 0.9980465173721313,
                                    "sentence_index": 0,
                                    "start": 29,
                                    "end": 38,
                                },
                                {
                                    "entity_type": "LOC",
                                    "entity_text": "California",
                                    "score": 0.9986708164215088,
                                    "sentence_index": 0,
                                    "start": 40,
                                    "end": 50,
                                },
                                {
                                    "entity_type": "PER",
                                    "entity_text": "Steve Jobs",
                                    "score": 0.9998300969600677,
                                    "sentence_index": 1,
                                    "start": 26,
                                    "end": 36,
                                },
                            ],
                        ]
                    },
                },
            },
        ),
        # Test case for Japanese (multiple documents)
        (
            {
                "data": {
                    "identifier": None,
                    "namespace": "ner",
                    "attributes": {
                        "content": [
                            "東京スカイツリーは、2012年に完成した東京都墨田区にある電波塔です。高さ634メートルで、日本で最も高い建造物として知られています。",
                            "任天堂は1889年に京都で創業された日本の会社で、マリオやゼルダなどの人気ゲームシリーズで有名です。現在は世界中でゲーム機やソフトウェアを販売しています。",
                            "村上春樹の小説「海辺のカフカ」は2002年に発表され、日本国内外で高い評価を受けました。物語は15歳の少年カフカの冒険を描いています。",
                            "富士山は静岡県と山梨県にまたがる日本最高峰の山で、標高は3776メートルです。2013年にユネスコ世界文化遺産に登録されました。",
                            "トヨタ自動車は1937年に愛知県で設立され、現在は世界最大級の自動車メーカーの一つです。ハイブリッド車プリウスなどの環境に配慮した車両で知られています。",
                        ]  # noqa
                    },
                    "parameters": {"language": "ja"},
                }
            },
            {
                "version": 1,
                "data": {
                    "identifier": None,
                    "namespace": "ner",
                    "attributes": {
                        "entities": [
                            [
                                {
                                    "entity_type": "LOC",
                                    "entity_text": "東京スカイツリー",
                                    "score": 0.9983153144518534,
                                    "sentence_index": 0,
                                    "start": 0,
                                    "end": 8,
                                },
                                {
                                    "entity_type": "LOC",
                                    "entity_text": "東京都墨田区",
                                    "score": 0.9964338392019272,
                                    "sentence_index": 0,
                                    "start": 20,
                                    "end": 26,
                                },
                            ],
                            [
                                {
                                    "entity_type": "ORG",
                                    "entity_text": "任天堂",
                                    "score": 0.9987733960151672,
                                    "sentence_index": 0,
                                    "start": 0,
                                    "end": 3,
                                },
                                {
                                    "entity_type": "LOC",
                                    "entity_text": "京都",
                                    "score": 0.9990463852882385,
                                    "sentence_index": 0,
                                    "start": 10,
                                    "end": 12,
                                },
                            ],
                            [
                                {
                                    "entity_type": "PER",
                                    "entity_text": "村上春樹",
                                    "score": 0.9997902810573578,
                                    "sentence_index": 0,
                                    "start": 0,
                                    "end": 4,
                                },
                                {
                                    "entity_type": "LOC",
                                    "entity_text": "日本",
                                    "score": 0.9967709183692932,
                                    "sentence_index": 0,
                                    "start": 27,
                                    "end": 29,
                                },
                                {
                                    "entity_type": "PER",
                                    "entity_text": "カフカ",
                                    "score": 0.9987940986951193,
                                    "sentence_index": 1,
                                    "start": 9,
                                    "end": 12,
                                },
                            ],
                            [
                                {
                                    "entity_type": "LOC",
                                    "entity_text": "富士山",
                                    "score": 0.999093234539032,
                                    "sentence_index": 0,
                                    "start": 0,
                                    "end": 3,
                                },
                                {
                                    "entity_type": "LOC",
                                    "entity_text": "静岡県",
                                    "score": 0.9971112807591757,
                                    "sentence_index": 0,
                                    "start": 4,
                                    "end": 7,
                                },
                                {
                                    "entity_type": "LOC",
                                    "entity_text": "山梨県",
                                    "score": 0.9849872986475626,
                                    "sentence_index": 0,
                                    "start": 8,
                                    "end": 11,
                                },
                                {
                                    "entity_type": "LOC",
                                    "entity_text": "日本",
                                    "score": 0.9677661061286926,
                                    "sentence_index": 0,
                                    "start": 16,
                                    "end": 18,
                                },
                                {
                                    "entity_type": "LOC",
                                    "entity_text": "ユネスコ",
                                    "score": 0.989531472325325,
                                    "sentence_index": 1,
                                    "start": 6,
                                    "end": 10,
                                },
                            ],
                            [
                                {
                                    "entity_type": "ORG",
                                    "entity_text": "トヨタ自動車",
                                    "score": 0.9966776669025421,
                                    "sentence_index": 0,
                                    "start": 0,
                                    "end": 6,
                                },
                                {
                                    "entity_type": "LOC",
                                    "entity_text": "愛知県",
                                    "score": 0.9996932744979858,
                                    "sentence_index": 0,
                                    "start": 13,
                                    "end": 16,
                                },
                            ],
                        ]
                    },
                },
            },
        ),
        # Test case for Korean (multiple documents)
        (
            {
                "data": {
                    "identifier": None,
                    "namespace": "ner",
                    "attributes": {
                        "content": [
                            "서울타워는 1975년에 완공된 서울특별시 용산구에 위치한 전망탑입니다. 남산 정상에 세워져 있어 서울의 상징적인 랜드마크로 알려져 있습니다.",
                            "삼성전자는 1969년에 설립된 한국의 대표적인 기업으로, 스마트폰과 반도체 분야에서 세계적인 기업으로 성장했습니다. 갤럭시 시리즈로 유명합니다.",
                            "백제문화단지는 충청남도 부여군에 위치한 역사 테마파크로, 2010년에 개장했습니다. 백제의 역사와 문화를 체험할 수 있는 다양한 시설을 갖추고 있습니다.",
                            "방탄소년단(BTS)은 2013년에 데뷔한 한국의 7인조 보이그룹으로, 전 세계적으로 큰 인기를 얻고 있습니다. 그들의 음악은 빌보드 차트에서 여러 차례 1위를 기록했습니다.",
                            "제주도는 대한민국 최남단에 위치한 화산섬으로, 2007년 유네스코 세계자연유산으로 지정되었습니다. 한라산과 아름다운 해변으로 유명한 관광지입니다.",
                        ]  # noqa
                    },
                    "parameters": {"language": "ko"},
                }
            },
            {
                "version": 1,
                "data": {
                    "identifier": None,
                    "namespace": "ner",
                    "attributes": {
                        "entities": [
                            [
                                {
                                    "entity_type": "LOC",
                                    "entity_text": "서울타워",
                                    "score": 0.9437261422475179,
                                    "sentence_index": 0,
                                    "start": 0,
                                    "end": 4,
                                },
                                {
                                    "entity_type": "LOC",
                                    "entity_text": "서울특별시",
                                    "score": 0.9993308782577515,
                                    "sentence_index": 0,
                                    "start": 17,
                                    "end": 22,
                                },
                                {
                                    "entity_type": "LOC",
                                    "entity_text": "용산구",
                                    "score": 0.9243932962417603,
                                    "sentence_index": 0,
                                    "start": 23,
                                    "end": 26,
                                },
                                {
                                    "entity_type": "LOC",
                                    "entity_text": "서울",
                                    "score": 0.9872727990150452,
                                    "sentence_index": 1,
                                    "start": 14,
                                    "end": 16,
                                },
                            ],
                            [
                                {
                                    "entity_type": "ORG",
                                    "entity_text": "삼성전자",
                                    "score": 0.9997698664665222,
                                    "sentence_index": 0,
                                    "start": 0,
                                    "end": 4,
                                }
                            ],
                            [
                                {
                                    "entity_type": "LOC",
                                    "entity_text": "백제문화단",
                                    "score": 0.997564509510994,
                                    "sentence_index": 0,
                                    "start": 0,
                                    "end": 5,
                                },
                                {
                                    "entity_type": "LOC",
                                    "entity_text": "충청남도",
                                    "score": 0.9952466487884521,
                                    "sentence_index": 0,
                                    "start": 8,
                                    "end": 12,
                                },
                                {
                                    "entity_type": "LOC",
                                    "entity_text": "부여군",
                                    "score": 0.9983508586883545,
                                    "sentence_index": 0,
                                    "start": 13,
                                    "end": 16,
                                },
                            ],
                            [
                                {
                                    "entity_type": "ORG",
                                    "entity_text": "방탄소년단",
                                    "score": 0.9995901942253113,
                                    "sentence_index": 0,
                                    "start": 0,
                                    "end": 5,
                                },
                                {
                                    "entity_type": "ORG",
                                    "entity_text": "BTS",
                                    "score": 0.9953851401805878,
                                    "sentence_index": 0,
                                    "start": 6,
                                    "end": 9,
                                },
                            ],
                            [
                                {
                                    "entity_type": "LOC",
                                    "entity_text": "제주",
                                    "score": 0.9961937665939331,
                                    "sentence_index": 0,
                                    "start": 0,
                                    "end": 2,
                                },
                                {
                                    "entity_type": "LOC",
                                    "entity_text": "대한민국",
                                    "score": 0.505710780620575,
                                    "sentence_index": 0,
                                    "start": 5,
                                    "end": 9,
                                },
                                {
                                    "entity_type": "ORG",
                                    "entity_text": "유네스코",
                                    "score": 0.9916230241457621,
                                    "sentence_index": 0,
                                    "start": 32,
                                    "end": 36,
                                },
                                {
                                    "entity_type": "LOC",
                                    "entity_text": "한라산",
                                    "score": 0.981324295202891,
                                    "sentence_index": 1,
                                    "start": 0,
                                    "end": 3,
                                },
                            ],
                        ]
                    },
                },
            },
        ),
    ],
)
def test_model_server_prediction(payload, expected_response):
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    response = requests.post(
        "http://serve:8000/ner/v1/predict",
        json=payload,
    )

    assert response.status_code == 200
    # TODO: assert score close to expected
    assert response.json() == expected_response


@pytest.mark.parametrize(
    "payload,expected_error_detail",
    [
        (
            {
                "data": {
                    "identifier": None,
                    "namespace": "ner",
                    "attributes": {
                        "content": "Irrelevant content because of invalid message value (nonsense)."
                    },
                    "parameters": {"language": "invalid_language"},
                }
            },
            "The language reference 'invalid_language' could not be mapped, or the language could not be inferred from the content.",  # noqa: E501
        ),
        (
            {
                "data": {
                    "identifier": None,
                    "namespace": "ner",
                    "attributes": {
                        "content": "Second example of irrelevant content because of invalid message value (empty string)."  # noqa: E501
                    },
                    "parameters": {"language": ""},
                }
            },
            "The language reference '' could not be mapped, or the language could not be inferred from the content.",  # noqa: E501
        ),
    ],
)
def test_model_server_prediction_invalid_language(payload, expected_error_detail):
    """Tests the language validation of the predict endpoint of a running ModelServer instance."""
    response = requests.post(
        "http://serve:8000/ner/v1/predict",
        json=payload,
    )

    assert response.status_code == 204
    assert response.text == ""
