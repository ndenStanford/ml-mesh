"""Main."""

# Source
from src.serve.server import get_model_server  # type: ignore[attr-defined]
from src.settings import get_settings


settings = get_settings()
model_server = get_model_server()  # type: ignore[call-arg]

if __name__ == "__main__":
    # launch server process(es)
    model_server.serve()
