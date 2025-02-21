"""Model server."""

# Standard Library
from typing import Any, Optional

# 3rd party libraries
import uvicorn
from fastapi import FastAPI

# Internal libraries
from onclusiveml.serving.rest.serve.params import ServingParams
from onclusiveml.serving.rest.serve.served_model import ServedModel
from onclusiveml.serving.rest.serve.server_utils import (
    TEST_MODEL_NAME,
    get_liveness_router,
    get_model_bio_router,
    get_model_predict_router,
    get_model_server_urls,
    get_readiness_router,
)


class ModelServer(FastAPI):
    """Model serving class.

    An enhanced FastAPI class with the ability to serve itself using a specified uvicorn
    configuration.
    Also includes readiness and liveness probe utilities and ServedModel integration.
    """

    def __init__(
        self,
        configuration: ServingParams,
        model: Optional[ServedModel] = None,
        *args: Any,
        **kwargs: Any,
    ):
        self.configuration = configuration
        if model is None:
            self.model = ServedModel(name=TEST_MODEL_NAME)
        else:
            self.model = model
        self.model_server_urls = get_model_server_urls(
            api_version=configuration.api_version, model_name=self.model.name
        )
        # if model is specified, ensure model loads are done in individual worker processes by
        # specifying start up behaviour
        if model is not None:
            if "on_startup" in kwargs:
                on_startup = kwargs.pop("on_startup")
                on_startup.append(model.load)
            else:
                on_startup = [model.load]
        else:
            on_startup = None

        super().__init__(
            *args,
            on_startup=on_startup,
            docs_url=self.model_server_urls.docs,
            redoc_url=self.model_server_urls.redoc,
            openapi_url=self.model_server_urls.openapi,
            **{**configuration.fastapi_settings.model_dump(), **kwargs},
        )
        # add default K8s liveness probe endpoint if desired
        if configuration.add_liveness:
            self.include_router(
                get_liveness_router(
                    model=self.model,
                    api_version=configuration.api_version,
                    betterstack_settings=configuration.betterstack_settings,
                    test_inference=configuration.liveness_sample_inference,
                )
            )
        # add default K8s readiness probe endpoint if desired
        if configuration.add_readiness:
            self.include_router(
                get_readiness_router(
                    model=self.model,
                    api_version=configuration.api_version,
                    test_inference=configuration.readiness_sample_inference,
                )
            )
        # ML services should expose the following additional routes implemented in the ServedModel:
        # - predict
        # - bio
        if configuration.add_model_predict:

            assert self.model is not None

            model_predict_router = get_model_predict_router(
                model=self.model, api_version=configuration.api_version
            )
            self.include_router(model_predict_router)

        if configuration.add_model_bio:

            assert self.model is not None

            model_bio_router = get_model_bio_router(
                model=self.model, api_version=configuration.api_version
            )
            self.include_router(model_bio_router)

    def serve(self) -> None:
        """Utility for running the fully configured app programmatically."""
        uvicorn.run(**self.configuration.uvicorn_settings.model_dump())
