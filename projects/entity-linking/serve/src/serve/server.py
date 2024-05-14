"""Model server getter."""

# 3rd party libraries
from fastapi import FastAPI
from pydantic import BaseSettings

# Internal libraries
from onclusiveml.serving.rest.observability import Instrumentator
from onclusiveml.serving.rest.serve import ModelServer

# Source
from src.serve.artifacts import BelaModelArtifacts
from src.serve.model import ServedBelaModel # type: ignore[attr-defined]
from src.settings import get_settings


settings = get_settings()


def get_model_server(artifacts: BelaModelArtifacts) -> ModelServer:
    """Utility method for prepping a fully configured model server instance ready to serve.
    Returns:
        ModelServer: Configured model server instance
    """
    # initialize model
    served_model_artifacts = artifacts
    cs_served_model = ServedBelaModel(served_model_artifacts=artifacts)
    # initialize model server
    model_server = ModelServer(configuration=settings, model=cs_served_model)
    Instrumentator.enable(model_server, app_name=settings.model_name)

    return model_server
