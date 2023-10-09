"""Main."""

# Source
from src.serve.artifacts import ServedModelArtifacts
from src.serve.server import get_model_server
from src.settings import get_settings


settings = get_settings()


if __name__ == "__main__":
    model_server = get_model_server(ServedModelArtifacts(settings))
    # launch server process(es)
    model_server.serve()
