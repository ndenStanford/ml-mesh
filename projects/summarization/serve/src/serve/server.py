"""Model server getter."""

# 3rd party libraries
from fastapi import FastAPI

# Internal libraries
from onclusiveml.serving.rest.observability import Instrumentator
from onclusiveml.serving.rest.serve import ModelServer

# Source
from src.serve.model import (  # type: ignore[attr-defined]
    SummarizationServedModel,
)
from src.settings import get_settings


settings = get_settings()


def get_model_server() -> FastAPI:
    """Instanciates model server.

    Args:
        settings (BaseSettings): application settings.
    """
    model_server = ModelServer(
        configuration=settings, model=SummarizationServedModel(name=settings.model_name)
    )
    if settings.enable_metrics:
        Instrumentator.enable(model_server, app_name=settings.model_name)

    return model_server
