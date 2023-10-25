"""Model server getter."""

# 3rd party libraries
from fastapi import FastAPI
from pydantic import BaseSettings

# Internal libraries
from onclusiveml.serving.rest.observability import Instrumentator
from onclusiveml.serving.rest.serve import ModelServer

# Source
from src.serve.model import EntityLinkingServedModel


def get_model_server(settings: BaseSettings) -> FastAPI:
    """Instanciates model server.

    Args:
        settings (BaseSettings): application settings.
    """
    model_server = ModelServer(
        configuration=settings, model=EntityLinkingServedModel(name=settings.model_name)
    )
    if settings.enable_metrics:
        Instrumentator.enable(model_server, app_name=settings.model_name)

    return model_server
