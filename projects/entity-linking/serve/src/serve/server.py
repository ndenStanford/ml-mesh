"""Model server getter."""

# 3rd party libraries
from fastapi import FastAPI
from pydantic import BaseSettings

# Internal libraries
from onclusiveml.serving.rest.observability import Instrumentator
from onclusiveml.serving.rest.serve import ModelServer

# Source
from src.serve.artifacts import ServedModelArtifacts
from src.serve.model import BELA # type: ignore[attr-defined]
from src.settings import get_settings


settings = get_settings()


def get_model_server(artifacts: ServedModelArtifacts) -> ModelServer:
    """Utility method for prepping a fully configured model server instance ready to serve.
    Returns:
        ModelServer: Configured model server instance
    """
    # initialize model
    served_model_artifacts = artifacts
    print("path1: ", served_model_artifacts.model_artifact_directory)
    cs_served_model = BELA(
        md_threshold=0.2,
        el_threshold=0.4, 
        checkpoint_name="wiki", 
        device="cuda:0",
        config_name="joint_el_mel_new",
        repo=served_model_artifacts.model_artifact_directory
    )
    print('SERVER STARTED')
    # initialize model server
    model_server = ModelServer(configuration=settings, model=cs_served_model)
    Instrumentator.enable(model_server, app_name=settings.model_name)

    return model_server
