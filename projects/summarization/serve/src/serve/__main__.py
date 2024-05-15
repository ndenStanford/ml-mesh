"""Main."""

# Source
from src.serve.server import get_model_server


model_server = get_model_server()

if __name__ == "__main__":
    # launch server process(es)
    model_server.serve()
