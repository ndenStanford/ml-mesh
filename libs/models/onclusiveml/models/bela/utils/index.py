# type: ignore
"""Redis index."""

# 3rd party libraries
from redis.client import Redis
from redis.commands.search.field import VectorField
from redis.exceptions import ResponseError


def get_index(client: Redis, index_name: str, vector_dimensions: int) -> None:
    """Creates Redis index if not exists.

    https://redis-py.readthedocs.io/en/stable/examples/search_vector_similarity_examples.html.

    Args:
        client (redis.client.Redis): Redis client
        index_name (str): Index name string
        vector_dimensions (int): Dimensions of a vector embedding
    """
    try:
        # check to see if index exists
        client.ft(index_name=index_name).info()
        print("Index already exists!")
    except ResponseError:
        # schema
        schema = (
            VectorField(
                name="embedding",
                algorithm="HNSW",
                attributes={
                    "TYPE": "FLOAT32",
                    "DIM": vector_dimensions,
                    "DISTANCE_METRIC": "COSINE",
                },
            ),
        )
        # create index
        client.ft(index_name=index_name).create_index(fields=schema)
