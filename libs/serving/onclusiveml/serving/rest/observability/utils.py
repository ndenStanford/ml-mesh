"""Utils."""

# Standard Library
from typing import Tuple

# 3rd party libraries
from prometheus_client.metrics_core import Metric
from starlette.requests import Request
from starlette.routing import Match


def get_path(request: Request) -> Tuple[str, bool]:
    """Retrieve the path of the matched route for the given request.

    If a full match is found among the application's routes, returns the path and True.
    If no full match is found, returns the URL path of the request and False.

    Args:
        request (Request): The HTTP request object containing information about
                           the incoming request.

    Returns:
        Tuple[str, bool]: A tuple containing two elements:
            - A string representing the path of the matched route if a full match is found,
              or the URL path of the request if no full match is found.
            - A boolean value that is True if a full match is found, and False otherwise.
    """
    for route in request.app.routes:
        match, child_scope = route.matches(request.scope)
        if match == Match.FULL:
            return route.path, True

    return request.url.path, False


def get_full_name(metric: Metric) -> str:
    """Get full metric name from OpenMetrics.

    Args:
        metric (Metric): A single metric family and its samples.

    Returns:
        str: full metric name.
    """
    full_name = ""
    full_name += metric._name
    if metric._type == "counter":
        full_name += "_total"
    return full_name
