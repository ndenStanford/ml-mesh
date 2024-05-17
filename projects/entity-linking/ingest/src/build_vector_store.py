# type: ignore
"""Create index and build vector store."""

# Standard Library
from typing import List

# ML libs
import torch
from torch.utils.data import DataLoader, Dataset

# 3rd party libraries
import numpy as np
from pydantic import BaseSettings
from redis import from_url
from redis.client import Redis
from redis.commands.search.field import VectorField
from redis.exceptions import ResponseError

# Source
from src.settings import get_settings


class WikiEmbeddings(Dataset):
    """Index and embeddings dataset."""

    def __init__(self, embeddings_file: str, index_file: str) -> None:
        self.embeddings_file = embeddings_file
        self.index_file = index_file
        self.embeddings = torch.load(self.embeddings_file)
        self.index = self._get_index()

    def _get_index(self) -> List:
        with open(self.index_file, "r") as f:
            index = [line.strip() for line in f]
        return index

    def __len__(self) -> int:
        return len(self.index)

    def __getitem__(self, idx: int) -> tuple:
        return (
            self.index[idx],
            self.embeddings[idx].numpy().astype(np.float16).tobytes(),
        )


def create_redis_index(
    vector_dimensions: int, client: Redis, settings: BaseSettings
) -> None:
    """Create Redis index.

    https://redis-py.readthedocs.io/en/stable/examples/search_vector_similarity_examples.html.

    Args:
        vector_dimensions (int): dimensions of a vector embedding
        client (redis.client.Redis): Redis client
        settings (pydantic.BaseSettings): Pydantic settings
    """
    try:
        # check to see if index exists
        client.ft(index_name=settings.INDEX_NAME).info()
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
        client.ft(index_name=settings.INDEX_NAME).create_index(fields=schema)


def write_to_redis_index(client: Redis, loader: DataLoader) -> None:
    """Write the data from loader to the redis index.

    Args:
        client (redis.client.Redis): Redis client
        loader (torch.utils.data.DataLoader): Dataset in pytorch DataLoader
    """
    pipe = client.pipeline()
    for idx, obj in loader:
        pipe.hset(name=idx[0], mapping={"embedding": obj[0]})
        pipe.execute()


def build_vector_store(settings: BaseSettings) -> None:
    """Build vector store.

    Args:
        settings (pydantic.BaseSettings): Pydantic settings
    """
    wiki_embeddings = WikiEmbeddings(
        embeddings_file=settings.EMBEDDINGS_FILE, index_file=settings.INDEX_FILE
    )
    loader = DataLoader(dataset=wiki_embeddings)
    try:
        client = from_url(url=settings.REDIS_CONNECTION_STRING)
    except ValueError as e:
        print(f"REDIS_CONNECTION_STRING is not valid: {e}")
        raise
    create_redis_index(
        vector_dimensions=wiki_embeddings.embeddings.shape[1],
        client=client,
        settings=settings,
    )
    write_to_redis_index(client=client, loader=loader)


if __name__ == "__main__":
    settings = get_settings()
    build_vector_store(settings)
