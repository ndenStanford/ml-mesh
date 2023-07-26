# Standard Library
from typing import Tuple

# 3rd party libraries
from starlette.requests import Request
from starlette.routing import Match


def get_path(request: Request) -> Tuple[str, bool]:
    for route in request.app.routes:
        match, child_scope = route.matches(request.scope)
        if match == Match.FULL:
            return route.path, True

    return request.url.path, False
