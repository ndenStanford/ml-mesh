"""Main."""

# Internal libraries
from onclusiveml.serving.rest.observability import Instrumentator
from onclusiveml.serving.rest.serve import ModelServer

# Source
from src.serve.model import EntityLinkingServedModel
from src.settings import get_settings


settings = get_settings()


if __name__ == "__main__":
    # launch server process(es)
    model_server = ModelServer(
        configuration=settings, model=EntityLinkingServedModel(name=settings.model_name)
    )
    Instrumentator.enable(model_server, app_name=settings.model_name)
    model_server.serve()
