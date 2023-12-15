"""Conftest."""

# 3rd party libraries
import pytest  # noqa

# Internal libraries
from onclusiveml.query_builder import (
    build_query,
    predict_entity_linking,
    predict_ner,
)
from onclusiveml.query_builder.settings import get_settings


settings = get_settings()


@pytest.fixture
def query_test():
    """Basic params."""
    company: str = "Apple"
    company_ticker: str = "AAPL"
    keywords: List[str] = ["Iphone"]
    return company, company_ticker, keywords


@pytest.fixture
def build_query_test(query_test):
    """Build query."""
    company, company_ticker, keywords = query_test
    return build_query(company, company_ticker, keywords, all_keywords=False)


@pytest.fixture
def evaluate_query_test(build_query_test):
    """Get results."""
    test_el, _, _ = build_query_test
    return test_el, settings.clustering_config, settings.scoring_config


@pytest.fixture
def test_el():
    """EL."""
    content = "The company Apple is great."
    return predict_entity_linking(content)


@pytest.fixture
def test_ner():
    """NER Params."""
    name: str = "Amazon"
    stock: str = "AMZN"
    content: str = (
        "The company "
        + name
        + " announced plans to revolutionize the market, which increased the stock "
        + stock
        + " by a huge 50%."
    )
    return predict_ner(content, [name, stock])


@pytest.fixture
def expected_query_builder():
    """Query Params."""
    return {
        "test_el": {
            "query": {
                "bool": {
                    "must": [
                        {
                            "nested": {
                                "path": "entities",
                                "query": {
                                    "bool": {
                                        "minimum_should_match": 1,
                                        "should": [
                                            {
                                                "bool": {
                                                    "must": [
                                                        {
                                                            "term": {
                                                                "entities.wiki_link": {
                                                                    "value": "https://www.wikidata.org/wiki/Q312"  # noqa
                                                                }
                                                            }
                                                        },
                                                        {
                                                            "match_phrase": {
                                                                "entities.text": "Apple"
                                                            }
                                                        },
                                                        {
                                                            "term": {
                                                                "entities.entity_type": {
                                                                    "value": "Organization"
                                                                }
                                                            }
                                                        },
                                                    ]
                                                }
                                            },
                                            {
                                                "bool": {
                                                    "must": [
                                                        {
                                                            "match_phrase": {
                                                                "entities.text": "AAPL"
                                                            }
                                                        },
                                                        {
                                                            "term": {
                                                                "entities.entity_type": {
                                                                    "value": "Organization"
                                                                }
                                                            }
                                                        },
                                                    ]
                                                }
                                            },
                                        ],
                                    }
                                },
                                "score_mode": "avg",
                            }
                        }
                    ],
                    "should": [
                        {
                            "nested": {
                                "path": "entities",
                                "query": {
                                    "bool": {
                                        "should": [
                                            {
                                                "match_phrase": {
                                                    "entities.text": "Iphone"
                                                }
                                            }
                                        ],
                                        "minimum_should_match": 0,
                                    }
                                },
                                "score_mode": "avg",
                            }
                        }
                    ],
                    "filter": [
                        {"term": {"lang": "en"}},
                        {"term": {"entities_wiki_version": "dataservices_v1"}},
                        {"term": {"source": "crawler"}},
                    ],
                }
            },
            "size": 1000,
        },
        "test_ner": {
            "query": {
                "bool": {
                    "must": [
                        {
                            "bool": {
                                "should": [
                                    {
                                        "nested": {
                                            "path": "entities",
                                            "query": {
                                                "bool": {
                                                    "should": [
                                                        {
                                                            "bool": {
                                                                "must": [
                                                                    {
                                                                        "match_phrase": {
                                                                            "entities.text": "Apple"
                                                                        }
                                                                    },
                                                                    {
                                                                        "term": {
                                                                            "entities.entity_type": {  # noqa
                                                                                "value": "Organization"  # noqa
                                                                            }
                                                                        }
                                                                    },
                                                                ]
                                                            }
                                                        }
                                                    ]
                                                }
                                            },
                                            "score_mode": "avg",
                                        }
                                    },
                                    {
                                        "nested": {
                                            "path": "entities",
                                            "query": {
                                                "bool": {
                                                    "should": [
                                                        {
                                                            "bool": {
                                                                "must": [
                                                                    {
                                                                        "match_phrase": {
                                                                            "entities.text": "AAPL"
                                                                        }
                                                                    },
                                                                    {
                                                                        "term": {
                                                                            "entities.entity_type": {  # noqa
                                                                                "value": "Organization"  # noqa
                                                                            }
                                                                        }
                                                                    },
                                                                ]
                                                            }
                                                        }
                                                    ]
                                                }
                                            },
                                            "score_mode": "avg",
                                        }
                                    },
                                ],
                                "minimum_should_match": 1,
                            }
                        },
                        {
                            "bool": {
                                "should": [
                                    {
                                        "nested": {
                                            "path": "entities",
                                            "query": {
                                                "bool": {
                                                    "should": [
                                                        {
                                                            "match_phrase": {
                                                                "entities.text": "Iphone"
                                                            }
                                                        }
                                                    ]
                                                }
                                            },
                                            "score_mode": "avg",
                                        }
                                    }
                                ],
                                "minimum_should_match": 0,
                            }
                        },
                    ],
                    "filter": [
                        {"term": {"lang": "en"}},
                        {"term": {"entities_wiki_version": "dataservices_v1"}},
                        {"term": {"source": "crawler"}},
                    ],
                }
            },
            "size": 1000,
        },
        "test_regex": {
            "query": {
                "bool": {
                    "filter": [
                        {"term": {"lang": "en"}},
                        {"term": {"entities_wiki_version": "dataservices_v1"}},
                        {"term": {"source": "crawler"}},
                    ],
                    "must": [
                        {
                            "bool": {
                                "should": [
                                    {"match_phrase": {"content": "apple"}},
                                    {"match_phrase": {"content": "aapl"}},
                                ],
                                "minimum_should_match": 1,
                            }
                        }
                    ],
                    "should": [{"match_phrase": {"content": "iphone"}}],
                }
            },
            "size": 1000,
        },
    }


@pytest.fixture
def test_query_builder(build_query_test):
    """Test builder."""
    test_el, test_ner, test_regex = build_query_test
    return test_el, test_ner, test_regex
