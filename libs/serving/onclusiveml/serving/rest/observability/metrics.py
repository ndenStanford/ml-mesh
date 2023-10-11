"""Metrics."""

# 3rd party libraries
from prometheus_client import Counter, Gauge, Histogram


INFO = Gauge(
    "fastapi_app_info", "FastAPI application information.", ["app_name", "pod_name"]
)
REQUESTS = Counter(
    "fastapi_requests_total",
    "Total count of requests by method and path.",
    ["method", "path", "app_name", "pod_name"],
)
RESPONSES = Counter(
    "fastapi_responses_total",
    "Total count of responses by method, path and status codes.",
    ["method", "path", "status_code", "app_name", "pod_name"],
)
REQUESTS_PROCESSING_TIME = Histogram(
    "fastapi_requests_duration_seconds",
    "Histogram of requests processing time by path (in seconds)",
    ["method", "path", "app_name", "pod_name"],
)
EXCEPTIONS = Counter(
    "fastapi_exceptions_total",
    "Total count of exceptions raised by path and exception type",
    ["method", "path", "exception_type", "app_name", "pod_name"],
)
REQUESTS_IN_PROGRESS = Gauge(
    "fastapi_requests_in_progress",
    "Gauge of requests by method and path currently being processed",
    ["method", "path", "app_name", "pod_name"],
)

REGISTERED_METRICS = [
    EXCEPTIONS,
    INFO,
    REQUESTS,
    REQUESTS_IN_PROGRESS,
    REQUESTS_PROCESSING_TIME,
    RESPONSES,
]
