"""Conftest."""

# Standard Library
import os

# 3rd party libraries
import pytest  # noqa


@pytest.fixture
def get_secret():
    """Get client id and secret."""
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    return client_id, client_secret


@pytest.fixture
def input_query():
    """Input query."""
    return """
        (apple  AND NOT  "Apple's Jade") OR  "Steve Jobs"  OR  "Tim Cook"  OR  "Angela Ahrends"  OR  "Eddie Cue"  OR  "Craig Federighi"  OR  "Jonathan Ive"  OR  "Luca Maestri"  OR  "Dan Riccio"  OR  "Phil Schiller"  OR  "Bruce Sewell"  OR  "Jeff Williams"  OR  "Paul Deneve"  OR  "Lisa Jackson"  OR  "Joel Podolny"  OR  "Johnny Srouji"  OR  "Denise Young Smith"
        """  # noqa: E501


@pytest.fixture
def expected_output():
    """Expected output for input query."""
    return {
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
                                    "source": "if (doc.containsKey('pagerank') && doc['pagerank'].size() > 0){ def pagerank = doc['pagerank'].value;  if (pagerank > 7)    { return params.pgrb_7_plus; }  else if (pagerank >= 4)    {  return params.pgrb_4_to_7; }  else if (pagerank >= 2)     { return params.pgrb_2_to_4; }  else     { return params.pgrb_less_than_2; }  } else  {return params.pgrb_none;}",  # noqa: E501
                                    "params": {
                                        "pgrb_7_plus": 13.0,
                                        "pgrb_4_to_7": 8.5,
                                        "pgrb_2_to_4": 3.5,
                                        "pgrb_less_than_2": 2.0,
                                        "pgrb_none": 1.0,
                                    },
                                }
                            },
                            "weight": 100.0,
                        },
                        {
                            "script_score": {
                                "script": {
                                    "source": "if (doc.containsKey('publication_details.publication_tier') && doc['publication_details.publication_tier'].size() > 0){ def publication_tier = doc['publication_details.publication_tier'].value; if (publication_tier.contains('1'))   { return params.pbb_1; }  else if (publication_tier.contains('2'))   { return params.pbb_2; }  else   { return params.pbb_1; }  }else { return params.pbb_none;} ",  # noqa: E501
                                    "params": {
                                        "pbb_1": 3.0,
                                        "pbb_2": 2.0,
                                        "pbb_3": 1.0,
                                        "pbb_none": 2.0,
                                    },
                                }
                            },
                            "weight": 50.0,
                        },
                        {
                            "script_score": {
                                "script": {
                                    "source": " def size = doc['content_size'].value; if (size < params.threshold)  { return params.factor; } else  { return 1;}",  # noqa: E501
                                    "params": {"threshold": 1000, "factor": 0},
                                }
                            }
                        },
                    ],
                    "boost_mode": "multiply",
                }
            }
        ]
    }  # noqa: E501
