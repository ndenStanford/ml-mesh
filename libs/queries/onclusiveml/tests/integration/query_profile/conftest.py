"""Conftest."""

# Standard Library

# 3rd party libraries
import pytest  # noqa


@pytest.fixture
def input_query():
    """Input query."""
    return """
        (apple  AND NOT  "Apple's Jade") OR  "Steve Jobs"  OR  "Tim Cook"  OR  "Angela Ahrends"  OR  "Eddie Cue"  OR  "Craig Federighi"  OR  "Jonathan Ive"  OR  "Luca Maestri"  OR  "Dan Riccio"  OR  "Phil Schiller"  OR  "Bruce Sewell"  OR  "Jeff Williams"  OR  "Paul Deneve"  OR  "Lisa Jackson"  OR  "Joel Podolny"  OR  "Johnny Srouji"  OR  "Denise Young Smith"
        """  # noqa: E501


@pytest.fixture
def input_query_id():
    """Input query id."""
    return "6bcd99ee-df08-4a7e-ad5e-5cdab4b558c3"


@pytest.fixture
def input_product_tool_version():
    """Input product tool version."""
    return "1"


@pytest.fixture
def input_media_api_query():
    """Input media api query."""
    return """{"query":{"advanced":{"terms":"(content:\\"Fidelity\\" || title:\\"Fidelity\\" || author:\\"Fidelity\\")"}},"source":"360","limit":100,"page":1,"filters":{"date":{"start":"2024-06-23 00:00","end":"2024-07-23 23:59","time_zone":"-04:00"},"lang":[],"pagerank":{"min":0,"max":10},"country":[],"domains":[],"es_filter":{"must_not":[{"prefix":{"licenses":{"value":"AGR:"}}},{"bool":{"must":[{"bool":{"must_not":{"term":{"market.country":"USA"}}}},{"bool":{"must":{"terms":{"domain.raw":["criticalmention.onclusive.com"]}}}}]}}],"must":[],"should":[{"bool":{"must_not":[{"exists":{"field":"licenses"}}],"must":[]}}],"should_minimum_match":1}},"exclude":{"country":[],"domains":["spain.onclusive.com","news.google.com"]},"sort":[{"published_on":{"order":"desc"}}],"return_fields":["id","ave","amplification","author","country","domain","lang","publication","published_on","reach","summary","title","url","score","media_type","pagerank","licenses","publication_details","sentiment","author_id","thumbnail_url","metadata"],"media_types":["web","print","tv","radio"]}"""  # noqa: E501


@pytest.fixture
def expected_query_id_output():
    """Expected output for id to boolean."""
    return """
        (apple  AND NOT  "Apple's Jade") OR  "Steve Jobs"  OR  "Tim Cook"  OR  "Angela Ahrends"  OR  "Eddie Cue"  OR  "Craig Federighi"  OR  "Jonathan Ive"  OR  "Luca Maestri"  OR  "Dan Riccio"  OR  "Phil Schiller"  OR  "Bruce Sewell"  OR  "Jeff Williams"  OR  "Paul Deneve"  OR  "Lisa Jackson"  OR  "Joel Podolny"  OR  "Johnny Srouji"  OR  "Denise Young Smith"
        """  # noqa: E501


@pytest.fixture
def expected_media_query():
    """Expected media api query."""
    return {
        "bool": {
            "filter": [
                {
                    "bool": {
                        "minimum_should_match": 1,
                        "should": [
                            {
                                "bool": {
                                    "minimum_should_match": 1,
                                    "should": [
                                        {
                                            "bool": {
                                                "must": [{"term": {"_type": "_doc"}}],
                                                "must_not": [
                                                    {"exists": {"field": "media_type"}}
                                                ],
                                            }
                                        },
                                        {"term": {"media_type": "web"}},
                                    ],
                                }
                            },
                            {
                                "bool": {
                                    "minimum_should_match": 1,
                                    "should": [
                                        {"term": {"_type": "_doc"}},
                                        {"term": {"media_type": "print"}},
                                    ],
                                }
                            },
                            {"terms": {"media_type": ["tv", "radio"]}},
                        ],
                    }
                },
                {
                    "bool": {
                        "should": [
                            {
                                "range": {
                                    "published_on": {
                                        "time_zone": "-04:00",
                                        "gte": "2024-06-23T00:00",
                                        "lte": "2024-07-23T23:59",
                                    }
                                }
                            },
                            {
                                "range": {
                                    "content_start_time": {
                                        "time_zone": "-04:00",
                                        "gte": "2024-06-23T00:00",
                                        "lte": "2024-07-23T23:59",
                                    }
                                }
                            },
                        ],
                        "minimum_should_match": 1,
                    }
                },
                {
                    "bool": {
                        "should": [
                            {"range": {"pagerank": {"gte": 0, "lte": 10}}},
                            {"exists": {"field": "station"}},
                        ],
                        "minimum_should_match": 1,
                    }
                },
                {
                    "bool": {
                        "must_not": [
                            {
                                "bool": {
                                    "must": [
                                        {"exists": {"field": "embargo_date"}},
                                        {"range": {"published_on": {"gte": "now"}}},
                                    ]
                                }
                            }
                        ]
                    }
                },
                {
                    "bool": {
                        "should": [
                            {
                                "bool": {
                                    "must": [{"terms": {"station.media_type": [1, 2]}}]
                                }
                            },
                            {"bool": {"must_not": [{"exists": {"field": "station"}}]}},
                        ],
                        "minimum_should_match": 1,
                    }
                },
                {
                    "bool": {
                        "minimum_should_match": 1,
                        "should": [
                            {
                                "bool": {
                                    "must_not": [{"exists": {"field": "licenses"}}],
                                    "must": [],
                                }
                            }
                        ],
                    }
                },
                {
                    "bool": {
                        "must_not": [
                            {"prefix": {"licenses": {"value": "AGR:"}}},
                            {
                                "bool": {
                                    "must": [
                                        {
                                            "bool": {
                                                "must_not": {
                                                    "term": {"market.country": "USA"}
                                                }
                                            }
                                        },
                                        {
                                            "bool": {
                                                "must": {
                                                    "terms": {
                                                        "domain.raw": [
                                                            "criticalmention.onclusive.com"
                                                        ]
                                                    }
                                                }
                                            }
                                        },
                                    ]
                                }
                            },
                        ]
                    }
                },
            ],
            "must_not": [
                {"term": {"domain.raw": "nla.onclusive.com"}},
                {"terms": {"domain": ["spain.onclusive.com", "news.google.com"]}},
                {"prefix": {"licenses": {"value": "AGR:"}}},
                {"term": {"licenses": "cedro_paywall"}},
            ],
            "must": [
                {
                    "query_string": {
                        "allow_leading_wildcard": False,
                        "query": '(content:"Fidelity" || title:"Fidelity" || author:"Fidelity")',
                        "fields": ["content", "title"],
                    }
                },
                {"exists": {"field": "content"}},
            ],
        }
    }


@pytest.fixture
def expected_output():
    """Expected output for input query."""
    return {
        "bool": {
            "must": [
                {
                    "function_score": {
                        "query": {
                            "bool": {
                                "should": [
                                    {
                                        "bool": {
                                            "must": [
                                                {
                                                    "multi_match": {
                                                        "query": "apple",
                                                        "fields": [
                                                            "content.split_word",
                                                            "title.split_word",
                                                        ],
                                                        "type": "best_fields",
                                                    }
                                                },
                                                {
                                                    "bool": {
                                                        "must_not": [
                                                            {
                                                                "multi_match": {
                                                                    "query": "Apple's Jade",
                                                                    "fields": [
                                                                        "content.split_word",
                                                                        "title.split_word",
                                                                    ],
                                                                    "type": "phrase",
                                                                }
                                                            }
                                                        ]
                                                    }
                                                },
                                            ]
                                        }
                                    },
                                    {
                                        "multi_match": {
                                            "query": "Steve Jobs",
                                            "fields": [
                                                "content.split_word",
                                                "title.split_word",
                                            ],
                                            "type": "phrase",
                                        }
                                    },
                                    {
                                        "multi_match": {
                                            "query": "Tim Cook",
                                            "fields": [
                                                "content.split_word",
                                                "title.split_word",
                                            ],
                                            "type": "phrase",
                                        }
                                    },
                                    {
                                        "multi_match": {
                                            "query": "Angela Ahrends",
                                            "fields": [
                                                "content.split_word",
                                                "title.split_word",
                                            ],
                                            "type": "phrase",
                                        }
                                    },
                                    {
                                        "multi_match": {
                                            "query": "Eddie Cue",
                                            "fields": [
                                                "content.split_word",
                                                "title.split_word",
                                            ],
                                            "type": "phrase",
                                        }
                                    },
                                    {
                                        "multi_match": {
                                            "query": "Craig Federighi",
                                            "fields": [
                                                "content.split_word",
                                                "title.split_word",
                                            ],
                                            "type": "phrase",
                                        }
                                    },
                                    {
                                        "multi_match": {
                                            "query": "Jonathan Ive",
                                            "fields": [
                                                "content.split_word",
                                                "title.split_word",
                                            ],
                                            "type": "phrase",
                                        }
                                    },
                                    {
                                        "multi_match": {
                                            "query": "Luca Maestri",
                                            "fields": [
                                                "content.split_word",
                                                "title.split_word",
                                            ],
                                            "type": "phrase",
                                        }
                                    },
                                    {
                                        "multi_match": {
                                            "query": "Dan Riccio",
                                            "fields": [
                                                "content.split_word",
                                                "title.split_word",
                                            ],
                                            "type": "phrase",
                                        }
                                    },
                                    {
                                        "multi_match": {
                                            "query": "Phil Schiller",
                                            "fields": [
                                                "content.split_word",
                                                "title.split_word",
                                            ],
                                            "type": "phrase",
                                        }
                                    },
                                    {
                                        "multi_match": {
                                            "query": "Bruce Sewell",
                                            "fields": [
                                                "content.split_word",
                                                "title.split_word",
                                            ],
                                            "type": "phrase",
                                        }
                                    },
                                    {
                                        "multi_match": {
                                            "query": "Jeff Williams",
                                            "fields": [
                                                "content.split_word",
                                                "title.split_word",
                                            ],
                                            "type": "phrase",
                                        }
                                    },
                                    {
                                        "multi_match": {
                                            "query": "Paul Deneve",
                                            "fields": [
                                                "content.split_word",
                                                "title.split_word",
                                            ],
                                            "type": "phrase",
                                        }
                                    },
                                    {
                                        "multi_match": {
                                            "query": "Lisa Jackson",
                                            "fields": [
                                                "content.split_word",
                                                "title.split_word",
                                            ],
                                            "type": "phrase",
                                        }
                                    },
                                    {
                                        "multi_match": {
                                            "query": "Joel Podolny",
                                            "fields": [
                                                "content.split_word",
                                                "title.split_word",
                                            ],
                                            "type": "phrase",
                                        }
                                    },
                                    {
                                        "multi_match": {
                                            "query": "Johnny Srouji",
                                            "fields": [
                                                "content.split_word",
                                                "title.split_word",
                                            ],
                                            "type": "phrase",
                                        }
                                    },
                                    {
                                        "multi_match": {
                                            "query": "Denise Young Smith",
                                            "fields": [
                                                "content.split_word",
                                                "title.split_word",
                                            ],
                                            "type": "phrase",
                                        }
                                    },
                                ],
                                "minimum_should_match": 1,
                            }
                        },
                        "functions": [
                            {
                                "script_score": {
                                    "script": {
                                        "source": " def pagerankBoost = 0.0; if (doc.containsKey('pagerank') && doc['pagerank'].size() > 0) { def pagerank = doc['pagerank'].value; if (pagerank > 7) { pagerankBoost = params.pgrb_7_plus; } else if (pagerank >= 4) { pagerankBoost = params.pgrb_4_to_7; } else if (pagerank >= 2) { pagerankBoost = params.pgrb_2_to_4; } else { pagerankBoost = params.pgrb_less_than_2; }} else { pagerankBoost = params.pgrb_none;} def publicationBoost = 0.0; if (doc.containsKey('publication_details.publication_tier') && doc['publication_details.publication_tier'].size() > 0) { def publication_tier = doc['publication_details.publication_tier'].value; if (publication_tier == '1') { publicationBoost = params.pbb_1; } else if (publication_tier == '2') { publicationBoost = params.pbb_2; } else {publicationBoost = params.pbb_3;}} else { publicationBoost = params.pbb_none;} def mediaTypeBoost = 0.0; if (doc.containsKey('media_type') && doc['media_type'].size() > 0) { def mediaType = doc['media_type'].value; def mediaTypeRanking = params.media_type_ranking; if (mediaTypeRanking.containsKey(mediaType)) { mediaTypeBoost = mediaTypeRanking[mediaType]; } else { mediaTypeBoost = mediaTypeRanking['other']; } } else { mediaTypeBoost = params.media_type_ranking['none']; } def starredPubBoost = 0.0; if (doc.containsKey('publication_details.id') && doc['publication_details.id'].size() > 0){ def publication_id = doc['publication_details.id'].value; def pubIdRanking = params.pub_id_ranking; if (pubIdRanking.containsKey(publication_id))     { starredPubBoost = pubIdRanking[publication_id]; } else     { starredPubBoost = pubIdRanking['other'];}} else {  starredPubBoost = params.pub_id_ranking['none'];} def mediaCategoryBoost = 0.0; if (doc.containsKey('publication_details.category') && doc['publication_details.category'].size() > 0) { def mediaCategory = doc['publication_details.category'].value; def mediaCategoryRanking = params.media_category_ranking; if (mediaCategoryRanking.containsKey(mediaCategory)) { mediaCategoryBoost = mediaCategoryRanking[mediaCategory]; } else { mediaCategoryBoost = mediaCategoryRanking['other']; } } else { mediaCategoryBoost = params.media_category_ranking['none']; } def pageNumberBoost = 0.0; if (doc.containsKey('print') && doc.containsKey('print.pageNumber') && doc['print.pageNumber'].size() > 0) {pageNumberBoost = 1/(1+doc['print.pageNumber'].value())} else { pageNumberBoost = params.pgnum_none; } def x = params.pgrb_weight * pagerankBoost + params.pbb_weight * publicationBoost + params.media_type_boost_weight * mediaTypeBoost * 1000 + params.starred_pub_boost_weight * starredPubBoost * 10 + params.media_category_boost_weight * mediaCategoryBoost * 100 + params.pgnum_boost_weight * pageNumberBoost; return sigmoid(x, params.sigmoid_k, params.sigmoid_a);",  # noqa: E501
                                        "params": {
                                            "pub_id_ranking": {
                                                "other": 0.1,
                                                "none": 0.1,
                                            },
                                            "media_category_ranking": {
                                                "other": 1.0,
                                                "none": 1.0,
                                            },
                                            "media_type_ranking": {
                                                "other": 1.0,
                                                "none": 1.0,
                                            },
                                            "pgrb_7_plus": 7.0,
                                            "pgrb_4_to_7": 5.0,
                                            "pgrb_2_to_4": 3.0,
                                            "pgrb_less_than_2": 2.0,
                                            "pgrb_none": 1.0,
                                            "pgrb_weight": 6.0,
                                            "pbb_1": 8.0,
                                            "pbb_2": 3.0,
                                            "pbb_3": 1.0,
                                            "pbb_none": 1.0,
                                            "pbb_weight": 6.0,
                                            "starred_pub_boost_weight": 10,
                                            "media_category_boost_weight": 8,
                                            "media_type_boost_weight": 9,
                                            "sigmoid_k": 50000,
                                            "sigmoid_a": 2,
                                            "pgnum_none": 1,
                                            "pgnum_boost_weight": 5,
                                        },
                                    }
                                },
                                "weight": 100.0,
                            },
                            {
                                "script_score": {
                                    "script": {
                                        "source": "if (doc.containsKey('publication_details.publication_tier') && doc['publication_details.publication_tier'].size() > 0 && doc.containsKey('content_size') && doc['content_size'].value < params.threshold) {    def publication_tier = doc['publication_details.publication_tier'].value;    if (publication_tier == '1' || publication_tier == '2')    { return 1; }   else     { return params.factor; }} else { return 1; }",  # noqa: E501
                                        "params": {"threshold": 1000, "factor": 0},
                                    }
                                }
                            },
                        ],
                        "boost_mode": "sum",
                    }
                }
            ]
        }
    }  # noqa: E501
