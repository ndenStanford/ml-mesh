"""Main."""

# Source
from src.model import EntityLinkingModel


class ServedModelParams(ServingBaseParams):
    """Serve model parameters."""

    model_name: str = "entity-linking"
    model_directory: Union[str, Path] = "."


if __name__ == "__main__":
    # launch server process(es)
    model_server = ModelServer(
        configuration=ServedModelParams(), model=EntityLinkingModel()
    )
    model_server.serve()
