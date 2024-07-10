"""Get articles."""

# Standard Library
from typing import List, Optional, Tuple, Union

# 3rd party libraries
from elasticsearch import Elasticsearch


def get_query_results(
    es: Elasticsearch, es_index: Union[List[str], str], query: dict
) -> Tuple[List[Optional[str]], List[Optional[float]]]:
    """Returns a list of articles with their associated scores.

    Args:
        es: the elasticsearch client
        query: the query built by the query builder

    Returns:
        Returns a list of strings and a list of floats
    """
    results = es.search(index=es_index, body=query)

    texts: List[Optional[str]] = []
    list_scores: List[Optional[float]] = []
    for k in range(len(results["hits"]["hits"])):
        texts.append(results["hits"]["hits"][k]["_source"]["content"])
        list_scores.append(results["hits"]["hits"][k]["_score"])
    return (texts, list_scores)


def remove_duplicates(doc_list: List[Optional[str]]) -> List[Optional[str]]:
    """Returns duplicate documents from a list of documents.

    Args:
        doc_list (list): A list of documents.

    Returns:
        list: A list of unique documents.
    """
    processed_docs = [
        doc.lower().strip() if doc is not None else None for doc in doc_list
    ]

    unique_docs = list(set(processed_docs))

    return unique_docs
