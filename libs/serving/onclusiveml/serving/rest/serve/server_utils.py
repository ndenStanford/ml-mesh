"""Serving helper methods."""

# Standard Library
import os
from typing import Callable, Dict

# 3rd party libraries
import requests
from fastapi import APIRouter, status

# Internal libraries
from onclusiveml.serving.rest.serve import ServedModel
from onclusiveml.serving.rest.serve.params import (
    BetterStackSettings,
    FastAPISettings,
)
from onclusiveml.serving.rest.serve.server_models import (
    LivenessProbeResponse,
    ModelServerURLs,
    ReadinessProbeResponse,
    ServedModelMethods,
)


TEST_MODEL_NAME = "no_model"


def get_model_server_urls(
    api_version: str = "v1", model_name: str = TEST_MODEL_NAME
) -> ModelServerURLs:
    """Utility for assembling the five currently supported Model server URLs.

    Supported URLS:
        - root
        - liveness
        - readiness
        - model predict
        - model bio

    Args:
        api_version (str, optional): The api version prefix, e.g. 'v1'. Defaults to ''.
        model_name (str, optional): The name of the ServedModel being served, if applicable.
            Defaults to ''.

    Returns:
        ModelServerURLs: A data model representing validated ModelServer URLs.
    """
    # ensure root url ends on '/' regardless of api_version
    root_url = os.path.join(f"/{model_name}", f"{api_version}/")

    liveness_url = os.path.join(root_url, "live/")  # ~ /{api_version}/live
    readiness_url = os.path.join(root_url, "ready/")  # ~ /{api_version}/readiness

    served_model_methods = ServedModelMethods()

    model_predict_url = os.path.join(root_url, f"{served_model_methods.predict}/")
    model_bio_url = os.path.join(root_url, f"{served_model_methods.bio}/")
    docs_url = os.path.join(root_url, "docs")
    redoc_url = os.path.join(root_url, "redoc")
    # dump into url data model with auto validation
    model_server_urls = ModelServerURLs(
        root=root_url,
        liveness=liveness_url,
        readiness=readiness_url,
        model_predict=model_predict_url,
        model_bio=model_bio_url,
        docs=docs_url,
        redoc=redoc_url,
    )

    return model_server_urls


def get_root_router(
    model: ServedModel,
    api_version: str = "v1",
    api_config: Dict = FastAPISettings().dict(),
) -> Callable:
    """Utility for a consistent api root endpoint."""
    root_router = APIRouter()

    model_server_urls = get_model_server_urls(
        api_version=api_version, model_name=model.name
    )

    @root_router.get(model_server_urls.root, status_code=status.HTTP_200_OK)
    async def root() -> Dict:
        return api_config

    return root_router


def get_liveness_router(
    model: ServedModel,
    betterstack_settings: BetterStackSettings,
    api_version: str = "v1",
) -> Callable:
    """Utility for a consistent liveness probe endpoint.

    For more information on how K8s uses these, see https://kubernetes.io/docs/tasks/...
    configure-pod-container/configure-liveness-readiness-startup-probes/

    Resources:
    For more information on how K8s uses these, see:
    https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/

    Args:
        api_version (str, optional): The api version string that will be used in the url.
            Defaults to "v1".
        betterstack_settings (BetterStackParams): The betterstack api settings.
            If enabled and configured correctly, every request to the liveness endpoint of the
            model server will trigger a ping to the betterstack project associated with the server.

    Returns:
        Callable: The FastAPI router object implementing the liveness endpoint
    """
    liveness_router = APIRouter()

    model_server_urls = get_model_server_urls(
        api_version=api_version, model_name=model.name
    )

    @liveness_router.get(
        model_server_urls.liveness,
        response_model=LivenessProbeResponse,
        status_code=status.HTTP_200_OK,
    )
    async def live() -> LivenessProbeResponse:
        if betterstack_settings.enable:

            requests.post(betterstack_settings.full_url)

        return LivenessProbeResponse()

    return liveness_router


def get_readiness_router(model: ServedModel, api_version: str = "v1") -> Callable:
    """Utility for a consistent readiness probe endpoint.

    For more information on how K8s uses these, see:
    https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/
    """
    readiness_router = APIRouter()

    model_server_urls = get_model_server_urls(
        api_version=api_version, model_name=model.name
    )

    @readiness_router.get(
        model_server_urls.readiness,
        response_model=ReadinessProbeResponse,
        status_code=status.HTTP_200_OK,
    )
    async def ready() -> ReadinessProbeResponse:
        return ReadinessProbeResponse()

    return readiness_router


def get_model_predict_router(model: ServedModel, api_version: str = "v1") -> APIRouter:
    """Utility to wrap a ServedModel's (subclass') instance's `predict` method into FastAPI router.

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
    model_server_urls = get_model_server_urls(
        api_version=api_version, model_name=model.name
    )
    # 'decorate' model method with parametrized fastapi route `post` wrapper
    model_predict_router.post(
        model_server_urls.model_predict,
        response_model=model.predict_response_model,
        status_code=status.HTTP_200_OK,
    )(model.predict)

    return model_predict_router


def get_model_bio_router(model: ServedModel, api_version: str = "v1") -> APIRouter:
    """Utility to wrap a ServedModel's (subclass') instance's `predict` method into FastAPI routers.

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
    # resolve url template
    model_server_urls = get_model_server_urls(
        api_version=api_version, model_name=model.name
    )
    # 'decorate' model method with parametrized fastapi route `get` wrapper.
    model_bio_router.get(
        model_server_urls.model_bio,
        response_model=model.bio_response_model,
        status_code=status.HTTP_200_OK,
    )(model.bio)

    return model_bio_router
