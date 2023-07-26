# Standard Library
import os

# 3rd party libraries
from fastapi import FastAPI

# Internal libraries
from onclusiveml.serving.rest.observability.handlers import metrics
from onclusiveml.serving.rest.observability.middlewares import (
    PrometheusMiddleware,
)
from onclusiveml.serving.rest.observability.opentelemetry import setting_otlp


OTLP_GRPC_ENDPOINT = os.environ.get("OTLP_GRPC_ENDPOINT", "http://tempo:4317")


class Instrumentator:
    def __init__(
        self,
        app: FastAPI,
        app_name: str = "FastAPI App",
        metrics_endpoint: str = "/metrics",
        setup_otl_exporter: bool = False,
    ):
        self.app = app
        self.app_name = app_name
        self.metrics_endpoint = metrics_endpoint
        self.setup_otl_exporter = setup_otl_exporter

    def setup(self) -> None:
        # Setting metrics middleware
        self.app.add_middleware(PrometheusMiddleware, app_name=self.app_name)
        self.app.add_route(self.metrics_endpoint, metrics)
        # Setting OpenTelemetry exporter
        if self.setup_otl_exporter:
            setting_otlp(self.app, self.app_name, OTLP_GRPC_ENDPOINT)

    @staticmethod
    def enable(app: FastAPI, app_name: str) -> None:
        Instrumentator(app, app_name=app_name).setup()
