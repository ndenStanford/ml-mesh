# type: ignore
"""Querying exmaple."""

# 3rd party libraries
import numpy as np
from pydantic import BaseSettings
from redis import from_url
from redis.commands.search.query import Query

# Source
from src.build_vector_store import WikiEmbeddings
from src.settings import get_settings


def run_querying_example(settings: BaseSettings, k: int) -> None:
    """Runs querying example.

    https://redis-py.readthedocs.io/en/stable/examples/search_vector_similarity_examples.html.

    Args:
        settings (pydantic.BaseSettings): Pydantic settings
        k (int): Number of neighbours
    """
    try:
        client = from_url(url=settings.REDIS_CONNECTION_STRING)
    except ValueError as e:
        print(f"REDIS_CONNECTION_STRING is not valid: {e}")
        raise
    wiki_embeddings = WikiEmbeddings(
        embeddings_file=settings.EMBEDDINGS_FILE, index_file=settings.INDEX_FILE
    )
    query = (
        Query(f"*=>[KNN {k} @embedding $query_vector as score]")
        .sort_by("score")
        .return_fields("id", "score")
        .paging(0, k)
        .dialect(2)
    )
    query_params = {
        "query_vector": np.random.rand(wiki_embeddings.embeddings.shape[1])
        .astype(np.float16)
        .tobytes()
    }
    print(client.ft(settings.INDEX_NAME).search(query, query_params).docs)


if __name__ == "__main__":
    settings = get_settings()
    run_querying_example(settings=settings, k=10)
