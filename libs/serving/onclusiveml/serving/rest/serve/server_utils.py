# Standard Library
from enum import Enum
from typing import Callable, Dict

# 3rd party libraries
from fastapi import APIRouter, status

# Internal libraries
from onclusiveml.serving.rest.params import FastAPISettings
from onclusiveml.serving.rest.serve import ServedModel
from onclusiveml.serving.rest.serve.server_models import (
    LivenessProbeResponse,
    ReadinessProbeResponse,
)


class ServedModelEndpoints(Enum):
    """Utility to track the methods that a ServedModel subclass must implement to integrate with the
    `create_model_enpoint` utility method (see below)."""

    predict: str = "predict"
    bio: str = "bio"


SERVING_ROOT_URL = "/{api_version}"
SERVING_LIVENESS_PROBE_URL = SERVING_ROOT_URL + "/live"
SERVING_READINESS_PROBE_URL = SERVING_ROOT_URL + "/ready"
SERVING_ML_MODEL_PREDICT_URL = (
    SERVING_ROOT_URL + "/model/{model_name}" + f"/{ServedModelEndpoints.predict.value}"
)
SERVING_ML_MODEL_BIO_URL = (
    SERVING_ROOT_URL + "/model/{model_name}" + f"/{ServedModelEndpoints.bio.value}"
)


def get_root_router(
    api_version: str = "v1", api_config: Dict = FastAPISettings().dict()
) -> Callable:
    """Utility for a consistent api root endpoint."""

    root_router = APIRouter()

    @root_router.get(
        SERVING_ROOT_URL.format(api_version=api_version), status_code=status.HTTP_200_OK
    )
    async def root() -> Dict:
        return api_config

    return root_router


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
    async def live() -> LivenessProbeResponse:
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
    async def ready() -> ReadinessProbeResponse:
        return ReadinessProbeResponse()

    return readiness_router


def get_model_predict_router(model: ServedModel, api_version: str = "v1") -> APIRouter:
    """Utility to wrap a ServedModel's (subclass') instance's `predict` method into FastAPI router
    compatible with the ModelServer class

    Args:
        model (ServedModel): The ServedModel instance implementing the endpoint logic and holding
            the
            - request & response model specifications as class attributes
            - model name
        api_version (str): The api version prefix. Will be used to construct the URL. See template
            variables
                - SERVING_ML_MODEL_PREDICT_URL
                - SERVING_ML_MODEL_BIO_URL
            for details
    Returns:
        model_predict_router (APIRouter): An APIRouter object that implements the model's `predict`
            method's logic as a functional FastAPI endpoint. Can be added directly as a route to a
            FastAPI and ModelServer instance.
    """

    model_predict_router = APIRouter()

    # resolve url template
    url = SERVING_ML_MODEL_PREDICT_URL.format(
        api_version=api_version, model_name=model.name
    )

    # 'decorate' model method with parametrized fastapi route `post` wrapper
    model_predict_router.post(
        url, response_model=model.predict_response_model, status_code=status.HTTP_200_OK
    )(model.predict)

    return model_predict_router


def get_model_bio_router(model: ServedModel, api_version: str = "v1") -> APIRouter:
    """Utility to wrap a ServedModel's (subclass') instance's `predict` method into FastAPI routers
    compatible with the ModelServer class

    Args:
        model (ServedModel): The ServedModel instance implementing the endpoint logic and holding
            the
                - response model specifications as a class attribute
                - model name
        api_version (str): The api version prefix. Will be used to construct the URL. See template
            variables
                - SERVING_ML_MODEL_PREDICT_URL
                - SERVING_ML_MODEL_BIO_URL
            for details
    Returns:
        model_bio_router (APIRouter): An APIRouter object that implements the model's `bio` method's
            logic as a functional FastAPI endpoint. Can be added directly as a route to a FastAPI
            and ModelServer instance.
    """

    model_bio_router = APIRouter()

    # resolve url template
    url = SERVING_ML_MODEL_BIO_URL.format(
        api_version=api_version, model_name=model.name
    )

    # 'decorate' model method with parametrized fastapi route `get` wrapper.
    model_bio_router.get(
        url, response_model=model.bio_response_model, status_code=status.HTTP_200_OK
    )(model.bio)

    return model_bio_router
