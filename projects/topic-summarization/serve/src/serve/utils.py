"""Topic summairization utility functions."""
from typing import Dict, Optional

import pandas as pd
import requests

from src.settings import get_settings

settings = get_settings()


def from_boolean_to_media_api(boolean_query: str, token: str) -> Optional[Dict]:
    """Invoke media API to translates a boolean query in media API format."""
    headers = {
        "accept": "*/*",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    json_data = {
        "name": "ml-query",
        "description": "used by ML team to translate queries from boolean to media API",
        "booleanQuery": boolean_query,
    }
    response = requests.put(
        f"{settings.MEDIA_API_URI}/v1/topics/{settings.ML_QUERY_ID}",
        headers=headers,
        json=json_data,
    )
    if response.status_code == 204:
        response = requests.get(
            f"{settings.MEDIA_API_URI}/v1/mediaContent/translate/mediaapi? \
                queryId={settings.ML_QUERY_ID}",
            headers=headers,
        )
        return response.json()
    else:
        return None


def query_translation(query: str) -> Dict:
    """Translates a boolean query in media API format."""
    token_request = requests.post(
        "https://login.microsoftonline.com/a4002d19-e8b4-4e6e-a00a-95d99cc7ef9a/oauth2/v2.0/token",
        {
            "client_id": settings.CLIENT_ID.get_secret_value(),
            "client_secret": settings.CLIENT_SECRET.get_secret_value(),
            "grant_type": "client_credentials",
            "scope": "c68b92d0-445f-4db0-8769-6d4ac5a4dbd8/.default",
        },
    )
    access_token: str = token_request.json()["access_token"]
    media_api_query = from_boolean_to_media_api(query, access_token)
    if media_api_query is not None and "es_query" in media_api_query["query"]:
        return {"bool": media_api_query["query"]["es_query"]}
    else:
        return {}


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
