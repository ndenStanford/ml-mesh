# Standard Library
from enum import Enum
from typing import Any, Callable, Dict, Literal

# 3rd party libraries
from fastapi import APIRouter, status

# Internal libraries
from onclusiveml.serving.rest.params import FastAPISettings
from onclusiveml.serving.rest.serve import ServedModel
from onclusiveml.serving.rest.serve.server_models import (
    LivenessProbeResponse,
    ReadinessProbeResponse,
)


SERVING_ROOT_URL = "/{api_version}"
SERVING_LIVENESS_PROBE_URL = SERVING_ROOT_URL + "/liveness"
SERVING_READINESS_PROBE_URL = SERVING_ROOT_URL + "/ready"
SERVING_ML_MODEL_PREDICT_URL = SERVING_ROOT_URL + "/model/{model_name}/predict"
SERVING_ML_MODEL_BIO_URL = SERVING_ROOT_URL + "/model/{model_name}/bio"


class ServedModelEndpoints(Enum):
    """Utility to track the methods that a ServedModel subclass must implement to integrate with the
    `create_model_enpoint` utility method (see below)."""

    predict: str = "predict"
    bio: str = "bio"


def get_root_router(
    api_version: str = "v1", api_config: Dict = FastAPISettings().dict()
) -> Callable:
    """API root url"""

    liveness_router = APIRouter()

    @liveness_router.get(
        SERVING_ROOT_URL.format(api_version=api_version), status_code=status.HTTP_200_OK
    )
    async def root() -> Dict:
        return api_config

    return liveness_router


def get_liveness_router(api_version: str = "v1") -> Callable:
    """Utility for a consistent liveness probe endpoint. For more information on how K8s uses these,
    see https://kubernetes.io/docs/tasks/configure-pod-container/...
    ...configure-liveness-readiness-startup-probes/"""

    liveness_router = APIRouter()

    @liveness_router.get(
        SERVING_LIVENESS_PROBE_URL.format(api_version=api_version),
        response_model=LivenessProbeResponse,
        status_code=status.HTTP_200_OK,
    )
    async def live() -> str:
        return LivenessProbeResponse()

    return liveness_router


def get_readiness_router(api_version: str = "v1") -> Callable:
    """Utility for a consistent readiness probe endpoint. For more information on how K8s uses
    these, see https://kubernetes.io/docs/tasks/configure-pod-container/...
    ...configure-liveness-readiness-startup-probes/"""

    readiness_router = APIRouter()

    @readiness_router.get(
        SERVING_READINESS_PROBE_URL.format(api_version=api_version),
        response_model=ReadinessProbeResponse,
        status_code=status.HTTP_200_OK,
    )
    async def ready() -> str:
        return ReadinessProbeResponse()

    return readiness_router


def create_model_endpoint(
    model: ServedModel, endpoint: Literal["predict", "bio"], api_version: str = "v1"
) -> APIRouter:
    """Utility to wrap model methods into FastAPI routers compatible with the ModelServer class

    Args:
        model (str): The ServedModel instance implementing the endpoint logic and holding the
            - request/response model specifications
            - model name
        endpoint (str): Reference to the ServedModel methods implementing the endpoint logic.
            Supports the two references defined in the ServedModelEndpoints class.
        api_version (str): The api version prefix. Will be used to construct the URL. See template
            variables
                - SERVING_ML_MODEL_PREDICT_URL
                - SERVING_ML_MODEL_BIO_URL
            for details
    Returns:
        model_endpoint: An APIRouter object that implements the model's method's logic as a
            functional FastAPI endpoint. Can be added directly as a route to a FastAPI and
            ModelServer instance.
    """

    model_router = APIRouter()
    # set fastapi router decorator params depending on endpoint
    if endpoint == ServedModelEndpoints.predict.value:
        model_router_request_type_decorator = model_router.post
        response_model = model.predict_response_model
        url_template = SERVING_ML_MODEL_PREDICT_URL
    elif endpoint == ServedModelEndpoints.bio.value:
        model_router_request_type_decorator = model_router.get
        response_model = model.bio_response_model
        url_template = SERVING_ML_MODEL_BIO_URL
    else:
        raise ValueError(
            f"Invalid endpoint specification {endpoint}. Only the the following model"
            f" endpoints are supported: {ServedModelEndpoints}."
        )

    # resolve url template
    url = url_template.format(api_version=api_version, model_name=model.name)

    # fetch model appropriate method
    model_method = getattr(model, endpoint)

    # decorate model method with parametrized fastapi route decorator
    @model_router_request_type_decorator(
        url,
        response_model=response_model,
        status_code=status.HTTP_200_OK,
    )
    async def model_endpoint(*args: Any, **kwargs: Any) -> str:
        model_response = model_method(*args, **kwargs)

        return model_response

    return model_router
