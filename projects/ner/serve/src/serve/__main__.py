"""Main."""

# Source
from src.serve.artifacts import ServedModelArtifacts
from src.serve.server import get_model_server


if __name__ == "__main__":
    model_server = get_model_server(ServedModelArtifacts())
    # launch server process(es)
    model_server.serve()
