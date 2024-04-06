"""Topic summairization utility functions."""
# Internal libraries

# Standard Library
from typing import Dict

# 3rd party libraries
import pandas as pd

# Internal libraries
# import requests
from onclusiveml.data.query_profile import MediaAPISettings, StringQueryProfile


def query_translation(query: str) -> Dict:
    """Translates a boolean query in media API format."""
    settings = MediaAPISettings()
    str_query = StringQueryProfile(string_query=query)
    es_query = str_query.es_query(settings)
    if es_query:
        es_query = {"bool": es_query}
    else:
        es_query = {}
    return es_query


def topic_global_query(
    start_time: pd.datetime, end_time: pd.datetime, topic_id: int, time_interval: str
) -> Dict:
    """Global trend query.

    time-series of total number of documents belonging to a topic.
    """
    query = {
        "size": 0,
        "query": {
            "bool": {
                "must": [
                    {
                        "nested": {
                            "path": "bertopic_topic",
                            "query": {
                                "bool": {
                                    "must": [
                                        {"match": {"bertopic_topic.topic_id": topic_id}}
                                    ]
                                }
                            },
                        }
                    }
                ],
                "filter": [
                    {"range": {"crawled_on": {"gte": start_time, "lte": end_time}}}
                ],
            }
        },
        "aggs": {
            "daily_doc_count": {
                "date_histogram": {
                    "field": "crawled_on",
                    "interval": time_interval,
                    "min_doc_count": 0,
                }
            }
        },
    }
    return query


def all_global_query(
    start_time: pd.datetime, end_time: pd.datetime, time_interval: str
) -> Dict:
    """Global trend query.

    Time-series of total number of documents.
    """
    query = {
        "size": 0,
        "query": {
            "bool": {
                "must": [
                    {
                        "nested": {
                            "path": "bertopic_topic",
                            "query": {
                                "bool": {
                                    "must": [
                                        {"exists": {"field": "bertopic_topic.topic_id"}}
                                    ]
                                }
                            },
                        }
                    }
                ],
                "filter": [
                    {"range": {"crawled_on": {"gte": start_time, "lte": end_time}}}
                ],
            }
        },
        "aggs": {
            "daily_doc_count": {
                "date_histogram": {
                    "field": "crawled_on",
                    "interval": time_interval,
                    "min_doc_count": 0,
                }
            }
        },
    }
    return query


def all_profile_boolean_query(
    translated_boolean_query: Dict,
    start_time: pd.datetime,
    end_time: pd.datetime,
    time_interval: str,
) -> Dict:
    """Local trend query.

    Time-series of total number of documents in the the scope of a profile.
    """
    query = {
        "size": 0,
        "query": {
            "bool": {
                "must": [
                    {
                        "nested": {
                            "path": "bertopic_topic",
                            "query": {
                                "bool": {
                                    "must": [
                                        {"exists": {"field": "bertopic_topic.topic_id"}}
                                    ]
                                }
                            },
                        }
                    }
                ],
                "filter": [
                    translated_boolean_query,
                    {"range": {"crawled_on": {"gte": start_time, "lte": end_time}}},
                ],
            }
        },
        "aggs": {
            "daily_doc_count": {
                "date_histogram": {
                    "field": "crawled_on",
                    "interval": time_interval,
                    "min_doc_count": 0,
                }
            }
        },
    }
    return query


def topic_profile_query(
    translated_boolean_query: Dict,
    start_time: pd.datetime,
    end_time: pd.datetime,
    topic_id: int,
    time_interval: str,
) -> Dict:
    """Local trend query.

    Time-series of total number of documents in the the scope
    of a profile belonging to a topic.
    """
    query = {
        "size": 0,
        "query": {
            "bool": {
                "must": [
                    {
                        "nested": {
                            "path": "bertopic_topic",
                            "query": {
                                "bool": {
                                    "must": [
                                        {"match": {"bertopic_topic.topic_id": topic_id}}
                                    ]
                                }
                            },
                        }
                    }
                ],
                "filter": [
                    translated_boolean_query,
                    {"range": {"crawled_on": {"gte": start_time, "lte": end_time}}},
                ],
            }
        },
        "aggs": {
            "daily_doc_count": {
                "date_histogram": {
                    "field": "crawled_on",
                    "interval": time_interval,
                    "min_doc_count": 0,
                }
            }
        },
    }
    return query


def topic_profile_documents_query(
    translated_boolean_query: Dict,
    start_time: pd.datetime,
    end_time: pd.datetime,
    topic_id: int,
) -> Dict:
    """Documents query.

    Returns list of documents of a given profile and topic.
    """
    query = {
        "size": 100,
        "query": {
            "bool": {
                "must": [
                    {
                        "nested": {
                            "path": "bertopic_topic",
                            "query": {
                                "bool": {
                                    "must": [
                                        {"match": {"bertopic_topic.topic_id": topic_id}}
                                    ]
                                }
                            },
                        }
                    }
                ],
                "filter": [
                    translated_boolean_query,
                    {"range": {"crawled_on": {"gte": start_time, "lte": end_time}}},
                ],
            }
        },
    }
    return query
