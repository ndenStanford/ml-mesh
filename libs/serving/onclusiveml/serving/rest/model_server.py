# Standard Library

# Standard Library
from typing import Any, Callable, Dict

# 3rd party libraries
import uvicorn
from fastapi import APIRouter, FastAPI, status

# Internal libraries
from onclusiveml.serving.params import FastAPISettings, ServingParams
from onclusiveml.serving.rest.models import (
    LivenessProbeResponse,
    ReadinessProbeResponse,
)
from onclusiveml.serving.rest.served_model import ServedModel


SERVING_LIVENESS_PROBE_URL = "liveness"
SERVING_READINESS_PROBE_URL = "ready"


def get_root_router(api_config: Dict = FastAPISettings.dict()) -> Callable:
    """API root url"""

    liveness_router = APIRouter()

    @liveness_router.get("/", status_code=status.HTTP_200_OK)
    async def root() -> Dict:
        return api_config

    return liveness_router


def get_liveness_router() -> Callable:
    """Utility for a consistent liveness probe endpoint. For more information on how K8s uses these,
    see https://kubernetes.io/docs/tasks/configure-pod-container/...
    ...configure-liveness-readiness-startup-probes/"""

    liveness_router = APIRouter()

    @liveness_router.get(
        f"/{SERVING_LIVENESS_PROBE_URL}",
        response_model=LivenessProbeResponse,
        status_code=status.HTTP_200_OK,
    )
    async def live() -> str:
        return LivenessProbeResponse()

    return liveness_router


def get_readiness_router() -> Callable:
    """Utility for a consistent readiness probe endpoint. For more information on how K8s uses
    these, see https://kubernetes.io/docs/tasks/configure-pod-container/...
    ...configure-liveness-readiness-startup-probes/"""

    readiness_router = APIRouter()

    @readiness_router.get(
        f"/{SERVING_READINESS_PROBE_URL}",
        response_model=ReadinessProbeResponse,
        status_code=status.HTTP_200_OK,
    )
    async def ready() -> str:
        return ReadinessProbeResponse()

    return readiness_router


class ModelServer(FastAPI):
    """An enhanced FastAPI class with the ability to serve itself using a specified uvicorn
    configuration.

    Also includes readiness and liveness probe utilities and ServedModel integration."""

    def __init__(
        self,
        configuration: ServingParams = ServingParams,
        model: ServedModel = ServedModel,
        *args: Any,
        **kwargs: Any,
    ):
        # ensure model loads are done in individual worker processes
        if "on_startup" in kwargs:
            on_startup = kwargs.pop("on_startup")
            on_startup.append(model.load)
        else:
            on_startup = [model.load]

        super().__init__(
            *args,
            on_startp=on_startup,
            **{**configuration.fastapi_settings.dict(), **kwargs},
        )

        self.configuration = configuration
        # add root endpoint with API meta data
        self.include_router(
            get_root_router(api_config=self.configuration.fastapi_settings)
        )
        # add default K8s liveness probe endpoint if desired
        if self.configuration.add_liveness:
            self.include_router(get_liveness_router())
        # add default K8s readiness probe endpoint if desired
        if self.configuration.add_readiness:
            self.include_router(get_readiness_router())

    def generate_uvicorn_config(self) -> uvicorn.Config:
        """Utility for generating and attaching a uvicorn configuration.
        Sources its parameters from the `configuration` arugment specified during initialization
        of the RESTApp instance."""

        self.uvicorn_configuration = uvicorn.Config(
            app=self,
            host=self.configuration.uvicorn_settings.host,  # "0.0.0.0",
            log_config=self.configuration.uvicorn_settings.log_config,  # str/Dict type. can be None
            port=self.configuration.uvicorn_settings.http_port,  # 8000
        )

        return self.uvicorn_configuration

    def serve(self) -> None:
        """Utility for running the fully configured app programmatically."""

        self.generate_uvicorn_config()

        server = uvicorn.Server(self.uvicorn_configuration)
        server.run()
