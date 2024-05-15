# type: ignore
"""Create index."""

# Standard Library
from typing import List

# ML libs
import torch
from torch.utils.data import DataLoader, Dataset

# 3rd party libraries
from pydantic import BaseSettings
from redis import from_url
from redis.client import Redis
from redis.commands.search.field import VectorField
from redis.exceptions import ResponseError

# Source
from src.settings import get_settings


def create_redis_index(
    vector_dimensions: int, client: Redis, settings: BaseSettings
) -> None:
    """Create Redis index.

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


class WikiEmbeddings(Dataset):
    """Index and embeddings dataset."""

    def __init__(self, settings: BaseSettings) -> None:
        self.settings = settings
        self.embeddings = torch.load(self.settings.EMBEDDINGS_FILE)
        self.index = self._get_index()

    def _get_index(self) -> List:
        with open(self.settings.INDEX_FILE, "r") as f:
            index = [line.strip() for line in f]
        return index

    def __len__(self) -> int:
        return len(self.index)

    def __getitem__(self, idx: int) -> tuple:
        return self.index[idx], self.embeddings[idx].numpy().tobytes()


if __name__ == "__main__":
    settings = get_settings()
    wiki_embeddings = WikiEmbeddings(settings=settings)
    loader = DataLoader(dataset=wiki_embeddings)
    client = from_url(url=settings.REDIS_CONNECTION_STRING)
    create_redis_index(
        vector_dimensions=wiki_embeddings.embeddings.shape[1],
        client=client,
        settings=settings,
    )
    pipe = client.pipeline()
    for idx, obj in loader:
        pipe.hset(name=idx[0], mapping={"embedding": obj[0]})
        pipe.execute()
