"""Main."""

# Source
from src.serve.artifacts import BelaModelArtifacts
from src.serve.server import get_model_server
from src.settings import get_settings


settings = get_settings()
model_server = get_model_server(BelaModelArtifacts(settings))

if __name__ == "__main__":
    # launch server process(es)
    model_server.serve()
