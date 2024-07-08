# type: ignore
"""Create index and build vector store."""

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSettings

# Source
from src.settings import get_settings
from src.utils.client import get_client
from src.utils.embeddings import get_embeddings
from src.utils.index import get_index, write_to_index


def build_vector_store(settings: OnclusiveBaseSettings) -> None:
    """Build vector store.

    Args:
        settings (pydantic.BaseSettings): Pydantic settings
    """
    wiki_embeddings, loader = get_embeddings(
        embeddings_file=settings.EMBEDDINGS_FILE, index_file=settings.INDEX_FILE
    )
    client = get_client(url=settings.REDIS_CONNECTION_STRING)
    get_index(
        client=client,
        index_name=settings.INDEX_NAME,
        vector_dimensions=wiki_embeddings.embeddings.shape[1],
    )
    write_to_index(client=client, loader=loader)


if __name__ == "__main__":
    settings = get_settings()
    build_vector_store(settings)
