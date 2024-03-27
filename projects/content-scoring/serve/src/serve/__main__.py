"""Model server."""

# Internal libraries
from onclusiveml.serving.rest.observability import Instrumentator
from onclusiveml.serving.rest.serve import ModelServer

# Source
from src.serve.artifacts import ServedModelArtifacts
from src.serve.model import ServedNERModel  # type: ignore[attr-defined]
from src.settings import get_settings


def get_model_server() -> ModelServer:
    """Utility to retrieve a fully configured model server instance.

    Returns:
        ModelServer: A model server instance.
    """
    settings = get_settings()
    artifacts = ServedModelArtifacts(settings)

    # initialize model
    ner_served_model = ServedNERModel(served_model_artifacts=artifacts)
    # initialize model server
    model_server = ModelServer(configuration=settings, model=ner_served_model)
    Instrumentator.enable(model_server, app_name=settings.model_name)

    return model_server


model_server = get_model_server()

if __name__ == "__main__":
    # launch server process(es)
    model_server.serve()
