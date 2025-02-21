"""Topic summairization utility functions."""

# Standard Library
from datetime import datetime
from typing import Dict

# 3rd party libraries
import pandas as pd


def all_profile_query(
    translated_boolean_query: Dict,
    start_time: datetime,
    end_time: datetime,
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
                    translated_boolean_query,
                ],
                "filter": [
                    {
                        "nested": {
                            "path": "bertopic_topic",
                            "query": {
                                "bool": {
                                    "filter": [
                                        {"exists": {"field": "bertopic_topic.topic_id"}}
                                    ]
                                }
                            },
                        }
                    },
                    {"range": {"crawled_on": {"gte": start_time, "lte": end_time}}},
                    {"term": {"lang": "en"}},
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


def topic_global_query(
    start_time: datetime, end_time: datetime, topic_id: int, time_interval: str
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
    start_time: datetime, end_time: datetime, time_interval: str
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
    start_time: datetime,
    end_time: datetime,
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
                    translated_boolean_query,
                ],
                "filter": [
                    {
                        "nested": {
                            "path": "bertopic_topic",
                            "query": {
                                "bool": {
                                    "filter": [
                                        {"exists": {"field": "bertopic_topic.topic_id"}}
                                    ]
                                }
                            },
                        }
                    },
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
    start_time: datetime,
    end_time: datetime,
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
                    translated_boolean_query,
                ],
                "filter": [
                    {
                        "nested": {
                            "path": "bertopic_topic",
                            "query": {
                                "bool": {
                                    "filter": [
                                        {"term": {"bertopic_topic.topic_id": topic_id}}
                                    ]
                                }
                            },
                        }
                    },
                    {"range": {"crawled_on": {"gte": start_time, "lte": end_time}}},
                    {"term": {"lang": "en"}},
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
    start_time: datetime,
    end_time: datetime,
    topic_id: int,
    size: int,
) -> Dict:
    """Documents query.

    Returns list of documents of a given profile and topic.
    """
    query = {
        "size": size,
        "query": {
            "bool": {
                "must": [
                    translated_boolean_query,
                ],
                "filter": [
                    {
                        "nested": {
                            "path": "bertopic_topic",
                            "query": {
                                "bool": {
                                    "filter": [
                                        {"term": {"bertopic_topic.topic_id": topic_id}}
                                    ]
                                }
                            },
                        }
                    },
                    {"range": {"crawled_on": {"gte": start_time, "lte": end_time}}},
                    {"term": {"lang": "en"}},
                ],
            }
        },
    }
    return query


def remove_weekends(results: Dict) -> Dict:
    """Time-series helper function."""
    df = pd.DataFrame(results)
    # remove weekends
    df["weekday_index"] = pd.to_datetime(df["key_as_string"]).apply(
        lambda x: x.weekday()
    )
    df = df[df["weekday_index"] <= 4]
    return df.to_dict("records")
