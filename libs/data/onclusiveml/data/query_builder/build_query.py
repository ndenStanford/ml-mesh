"""Query builder."""

# Standard Library
from typing import Any, Dict, List, Tuple, Union

# Internal libraries
from onclusiveml.data.query_builder.get_el import predict_entity_linking
from onclusiveml.data.query_builder.get_ner import predict_ner


def build_query(
    stock_name: str,
    stock_ticker: str,
    keywords: List[str],
    all_keywords: bool = False,
    size: int = 1000,
) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    """Builds queries based on stock information, keywords, and other parameters.

    Will produce 3 queries:
    - query_el: with entity-linking based solution with a mandatory entity with associated link
    for the company name
    - query_ner: with an entity based solution with a mandatory entity for the company name
    - query_regex: with a text matching solution with a mandatory text match of the name

    Args:
        stock_name (str): Name of the stock/company.
        stock_ticker (str): Ticker symbol of the stock/company.
        keywords (List[str]): List of keywords related to the stock/company.
        all_keywords (bool, optional): Flag to indicate using all keywords. Defaults to False.
        size (int, optional): Size parameter for query. Defaults to 1000.

    Returns:
        Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]: Tuple containing query results.
    """
    content_wiki_link: str = "The company " + stock_name + " is great."
    wiki_link: str = predict_entity_linking(content_wiki_link, language="en")

    content_NER: str = (
        "The company "
        + stock_name
        + " announced plans to revolutionize the market, which increased the stock "
        + stock_ticker
        + " by a huge 50%."
    )
    content_keywords: str = (
        "This company is best described by "
        + ", ".join(keywords)
        + ", which have been provided."
    )

    entities: List[str] = predict_ner(content_NER, [stock_name, stock_ticker])
    entities_keywords: List[str] = predict_ner(content_keywords, keywords)
    non_entities_keywords: List[str] = list(set(keywords) - set(entities_keywords))

    if stock_ticker not in entities:
        non_entities_keywords.append(stock_ticker)

    query_el: Union[Dict[str, Any], List[Dict[str, Any]]] = {}  # Adjusted annotation
    query_ner: Union[Dict[str, Any], List[Dict[str, Any]]] = {}  # Adjusted annotation
    query_regex: Dict[str, Any] = {}

    if wiki_link:
        nested_queries = []
        should_queries = []

        if all_keywords:
            nested_queries.append(
                {
                    "nested": {
                        "path": "entities",
                        "query": {
                            "bool": {
                                "must": [
                                    {"match_phrase": {"entities.text": entity}}
                                    for entity in entities_keywords
                                ]
                            }
                        },
                        "score_mode": "avg",
                    }
                }
            )

            nested_queries.extend(
                [
                    {"match": {"content": content.lower()}}
                    for content in non_entities_keywords
                ]
            )

        else:
            should_queries.append(
                {
                    "nested": {
                        "path": "entities",
                        "query": {
                            "bool": {
                                "should": [
                                    {"match_phrase": {"entities.text": entity}}
                                    for entity in entities_keywords
                                ],
                                "minimum_should_match": 0,
                            }
                        },
                        "score_mode": "avg",
                    }
                }
            )

            should_queries.extend(
                [
                    {"match": {"content": content.lower()}}
                    for content in non_entities_keywords
                ]
            )

        nested_queries.append(
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
                                                        "value": wiki_link
                                                    }
                                                }
                                            },
                                            {
                                                "match_phrase": {
                                                    "entities.text": stock_name
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
                                                    "entities.text": stock_ticker
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
        )

        query_el = {
            "query": {
                "bool": {
                    "must": nested_queries,
                    "should": should_queries if should_queries else [],
                    "filter": [
                        {"term": {"lang": "en"}},
                        {"term": {"entities_wiki_version": "dataservices_v1"}},
                        {"term": {"source": "crawler"}},
                    ],
                }
            },
            "size": size,
        }

    else:
        query_el = {}

    if entities:
        nested_queries_entities = [
            {
                "nested": {
                    "path": "entities",
                    "query": {
                        "bool": {
                            "should": [
                                {
                                    "bool": {
                                        "must": [
                                            {"match_phrase": {"entities.text": entity}},
                                            {
                                                "term": {
                                                    "entities.entity_type": {
                                                        "value": "Organization"
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
            }
            for entity in entities
        ]

        query_ner = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "bool": {
                                "should": nested_queries_entities,
                                "minimum_should_match": 1,
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
            "size": size,
        }

        if all_keywords:
            nested_queries_entities_keywords = [
                {
                    "nested": {
                        "path": "entities",
                        "query": {
                            "bool": {
                                "should": [{"match_phrase": {"entities.text": entity}}]
                            }
                        },
                        "score_mode": "avg",
                    }
                }
                for entity in entities_keywords
            ]

            nested_queries_non_entities_keywords = [
                {"match": {"content": content.lower()}}
                for content in non_entities_keywords
            ]

            query_ner["query"]["bool"]["must"].append(
                {
                    "bool": {
                        "should": nested_queries_entities_keywords
                        + nested_queries_non_entities_keywords,
                        "minimum_should_match": len(entities_keywords)
                        + len(non_entities_keywords),
                    }
                }
            )

        else:
            nested_queries_entities_keywords = [
                {
                    "nested": {
                        "path": "entities",
                        "query": {
                            "bool": {
                                "should": [{"match_phrase": {"entities.text": entity}}]
                            }
                        },
                        "score_mode": "avg",
                    }
                }
                for entity in entities_keywords
            ]

            nested_queries_non_entities_keywords = [
                {"match": {"content": content.lower()}}
                for content in non_entities_keywords
            ]

            query_ner["query"]["bool"]["must"].append(
                {
                    "bool": {
                        "should": nested_queries_entities_keywords
                        + nested_queries_non_entities_keywords,
                        "minimum_should_match": 0,
                    }
                }
            )

    else:
        query_ner = {}

    list_words = keywords
    list_words.reverse()
    must_queries = [
        {
            "bool": {
                "should": [
                    {"match_phrase": {"content": stock_name.lower()}},
                    {"match_phrase": {"content": stock_ticker.lower()}},
                ],
                "minimum_should_match": 1,
            }
        }
    ]
    content_queries = [
        {"match_phrase": {"content": content.lower()}} for content in list_words
    ]

    query_bool: Dict[str, Any] = {
        "bool": {
            "filter": [
                {"term": {"lang": "en"}},
                {"term": {"entities_wiki_version": "dataservices_v1"}},
                {"term": {"source": "crawler"}},
            ]
        }
    }

    if all_keywords:
        query_bool["bool"]["must"] = must_queries + content_queries
    else:
        query_bool["bool"]["must"] = must_queries
        query_bool["bool"]["should"] = content_queries

    query_regex = {"query": query_bool, "size": size}

    return query_el, query_ner, query_regex
