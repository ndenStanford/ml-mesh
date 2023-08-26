"""Instrumentator."""

# 3rd party libraries
from fastapi import FastAPI

# Internal libraries
from onclusiveml.serving.rest.observability.handlers import metrics
from onclusiveml.serving.rest.observability.middlewares import (
    PrometheusMiddleware,
)


class Instrumentator:
    """Metrics collection instrumentator."""

    def __init__(
        self,
        app: FastAPI,
        app_name: str = "FastAPI App",
        metrics_endpoint: str = "/metrics",
    ):
        """An entry point to metrics instrumentation.

        Args:
            app (FastAPI): The FastAPI app.
            app_name (str, optional): The name of the app. Defaults to "FastAPI App".
            metrics_endpoint (str, optional): The endpoint for metrics. Defaults to "/metrics".
        """
        self.app = app
        self.app_name = app_name
        self.metrics_endpoint = metrics_endpoint

    def setup(self) -> "Instrumentator":
        """Set up Instrumentator with Prometheus Middlewares and routes.

        Returns:
            Instrumentator: Returns the Instrumentator instance for chaining.
        """
        # Setting metrics middleware
        self.app.add_middleware(PrometheusMiddleware, app_name=self.app_name)
        self.app.add_route(self.metrics_endpoint, metrics)
        return self

    @staticmethod
    def enable(app: FastAPI, app_name: str) -> "Instrumentator":
        """Class Method to conveniently enable Instrumentator on a FastAPI app.

        Args:
            app (FastAPI): The FastAPI app.
            app_name (str): The name of the app.

        Returns:
            Instrumentator: Returns the Instrumentator instance for chaining.
        """
        return Instrumentator(app, app_name=app_name).setup()
