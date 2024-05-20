# type: ignore
"""Querying exmaple."""

# Standard Library
from typing import Optional

# 3rd party libraries
import numpy as np
from pydantic import BaseSettings
from redis import from_url
from redis.commands.search.query import Query

# Source
from src.build_vector_store import WikiEmbeddings
from src.settings import get_settings


def run_querying_example(
    settings: BaseSettings, k: int, query_index: Optional[str] = None
) -> None:
    """Runs querying example.

    https://redis-py.readthedocs.io/en/stable/examples/search_vector_similarity_examples.html.

    Args:
        settings (pydantic.BaseSettings): Pydantic settings
        k (int): Number of neighbours
        query_index (str): Optional query index in form of wikidata item identifier, default None
    """
    try:
        client = from_url(url=settings.REDIS_CONNECTION_STRING)
    except ValueError as e:
        print(f"REDIS_CONNECTION_STRING is not valid: {e}")
        raise
    query = (
        Query(f"*=>[KNN {k} @embedding $query_vector as score]")
        .sort_by("score")
        .return_fields("id", "score")
        .paging(0, k)
        .dialect(2)
    )
    if query_index:
        wiki_embeddings = WikiEmbeddings(
            embeddings_file=settings.EMBEDDINGS_FILE, index_file=settings.INDEX_FILE
        )
        if query_index not in wiki_embeddings.index:
            raise ValueError(
                f"Query_index {query_index} is not in the embeddings index."
            )
        query_vector = (
            wiki_embeddings.embeddings[wiki_embeddings.index.index(query_index)]
            .numpy()
            .astype(np.float32)
            .tobytes()
        )
    else:
        query_vector = (
            np.random.rand(settings.EMBEDDINGS_SHAPE[1]).astype(np.float32).tobytes()
        )
    query_params = {"query_vector": query_vector}
    print(client.ft(settings.INDEX_NAME).search(query, query_params).docs, sep="\n")


if __name__ == "__main__":
    settings = get_settings()
    run_querying_example(settings=settings, k=5)  # query_index="Q99" California
