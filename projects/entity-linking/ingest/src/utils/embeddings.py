# type: ignore
"""Gets embeddings data and data loader."""

# Standard Library
from typing import List, Tuple

# ML libs
import torch
from torch.utils.data import DataLoader, Dataset

# 3rd party libraries
import numpy as np


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

    def __getitem__(self, idx: int) -> Tuple[str, bytes]:
        return (
            self.index[idx],
            self.embeddings[idx].numpy().astype(np.float32).tobytes(),
        )


def get_embeddings(
    embeddings_file: str, index_file: str
) -> Tuple[WikiEmbeddings, DataLoader]:
    """Gets embeddings.

    Args:
        embeddings_file (str): Location of the embeddings file, absolute path
        index_file (str): Location of the index file, absolute path

    Returns:
        torch.utils.data.Dataset: Embeddings dataset
        torch.utils.data.DataLoader: Embeddings data loader
    """
    wiki_embeddings = WikiEmbeddings(
        embeddings_file=embeddings_file, index_file=index_file
    )
    loader = DataLoader(dataset=wiki_embeddings)
    return wiki_embeddings, loader
