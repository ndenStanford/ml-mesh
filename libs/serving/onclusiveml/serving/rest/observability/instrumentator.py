# 3rd party libraries
from fastapi import FastAPI

# Internal libraries
from onclusiveml.serving.rest.observability.handlers import metrics
from onclusiveml.serving.rest.observability.middlewares import (
    PrometheusMiddleware,
)


class Instrumentator:
    def __init__(
        self,
        app: FastAPI,
        app_name: str = "FastAPI App",
        metrics_endpoint: str = "/metrics",
    ):
        self.app = app
        self.app_name = app_name
        self.metrics_endpoint = metrics_endpoint

    def setup(self) -> "Instrumentator":
        # Setting metrics middleware
        self.app.add_middleware(PrometheusMiddleware, app_name=self.app_name)
        self.app.add_route(self.metrics_endpoint, metrics)
        return self

    @staticmethod
    def enable(app: FastAPI, app_name: str) -> "Instrumentator":
        return Instrumentator(app, app_name=app_name).setup()
