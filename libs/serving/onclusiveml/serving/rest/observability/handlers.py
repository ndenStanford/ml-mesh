# 3rd party libraries
from prometheus_client import REGISTRY
from prometheus_client.openmetrics.exposition import (
    CONTENT_TYPE_LATEST,
    generate_latest,
)
from starlette.requests import Request
from starlette.responses import Response


def metrics(request: Request) -> Response:
    """Returns the Prometheus metrics in the latest OpenMetrics format.

    Args:
        request (Request): The incoming Starlette request object.

    Returns:
        Response: A Starlette response containing the Prometheus metrics in the
        latest OpenMetrics format with the appropriate Content-Type header.
    """
    return Response(
        generate_latest(REGISTRY), headers={"Content-Type": CONTENT_TYPE_LATEST}
    )
