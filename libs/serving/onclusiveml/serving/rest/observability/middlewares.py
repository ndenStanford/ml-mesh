# Standard Library
import time

# 3rd party libraries
from opentelemetry import trace
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from starlette.types import ASGIApp

# Internal libraries
from onclusiveml.serving.rest.observability.metrics import (
    EXCEPTIONS,
    INFO,
    REQUESTS,
    REQUESTS_IN_PROGRESS,
    REQUESTS_PROCESSING_TIME,
    RESPONSES,
)
from onclusiveml.serving.rest.observability.utils import get_path


class PrometheusMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, app_name: str = "fastapi-app") -> None:
        super().__init__(app)
        self.app_name = app_name
        INFO.labels(app_name=self.app_name).inc()

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        method = request.method
        path, is_handled_path = get_path(request)

        if not is_handled_path:
            return await call_next(request)

        REQUESTS_IN_PROGRESS.labels(
            method=method, path=path, app_name=self.app_name
        ).inc()
        REQUESTS.labels(method=method, path=path, app_name=self.app_name).inc()
        before_time = time.perf_counter()
        try:
            response = await call_next(request)
        except BaseException as e:
            status_code = HTTP_500_INTERNAL_SERVER_ERROR
            EXCEPTIONS.labels(
                method=method,
                path=path,
                exception_type=type(e).__name__,
                app_name=self.app_name,
            ).inc()
            raise e from None
        else:
            status_code = response.status_code
            after_time = time.perf_counter()
            # retrieve trace id for exemplar
            span = trace.get_current_span()
            trace_id = trace.format_trace_id(span.get_span_context().trace_id)

            REQUESTS_PROCESSING_TIME.labels(
                method=method, path=path, app_name=self.app_name
            ).observe(after_time - before_time, exemplar={"TraceID": trace_id})
        finally:
            RESPONSES.labels(
                method=method,
                path=path,
                status_code=status_code,
                app_name=self.app_name,
            ).inc()
            REQUESTS_IN_PROGRESS.labels(
                method=method, path=path, app_name=self.app_name
            ).dec()

        return response
