"""Instrumentator."""

# 3rd party libraries
from fastapi import FastAPI

# Internal libraries
from onclusiveml.serving.rest.observability.handlers import (
    metrics,
    multiprocess_metrics,
)
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
        multiprocess: bool = False,
    ):
        """An entry point to metrics instrumentation.

        Args:
            app (FastAPI): The FastAPI app.
            app_name (str, optional): The name of the app. Defaults to "FastAPI App".
            metrics_endpoint (str, optional): The endpoint for metrics. Defaults to "/metrics".
            multiprocess (bool, optional): Flag to enable multiprocess metrics. Defaults to False.
        """
        self.app = app
        self.app_name = app_name
        self.metrics_endpoint = metrics_endpoint
        self.multiprocess = multiprocess

    def setup(self) -> "Instrumentator":
        """Set up Instrumentator with Prometheus Middlewares and routes.

        Returns:
            Instrumentator: Returns the Instrumentator instance for chaining.
        """
        # Setting metrics middleware
        self.app.add_middleware(PrometheusMiddleware, app_name=self.app_name)
        # Adding the route endpoint if the prometheus client is in the 'multiprocess' mode.
        if self.multiprocess:
            self.app.add_route(self.metrics_endpoint, multiprocess_metrics)
        else:
            self.app.add_route(self.metrics_endpoint, metrics)
        return self

    @staticmethod
    def enable(
        app: FastAPI, app_name: str, multiprocess: bool = False
    ) -> "Instrumentator":
        """Class Method to conveniently enable Instrumentator on a FastAPI app.

        Args:
            app (FastAPI): The FastAPI app.
            app_name (str): The name of the app.
            multiprocess (bool, optional): Flag to enable multiprocess metrics. Defaults to False.

        Returns:
            Instrumentator: Returns the Instrumentator instance for chaining.
        """
        return Instrumentator(app, app_name=app_name, multiprocess=multiprocess).setup()
