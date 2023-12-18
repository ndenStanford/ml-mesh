"""Model server."""

# Internal libraries
from onclusiveml.serving.rest.observability import Instrumentator
from onclusiveml.serving.rest.serve import ModelServer

# Source
from src.serve.artifacts import ServedModelArtifacts
from src.serve.model import ServedTopicModel
from src.settings import get_settings


settings = get_settings()


def get_model_server(artifacts: ServedModelArtifacts) -> ModelServer:
    """Utility method for prepping a fully configured model server instance ready to serve.

    Returns:
        ModelServer: Configured model server instance
    """
    # initialize model
    sent_served_model = ServedTopicModel(served_model_artifacts=artifacts)
    # initialize model server
    model_server = ModelServer(configuration=settings, model=sent_served_model)
    Instrumentator.enable(model_server, app_name=settings.model_name)

    return model_server
