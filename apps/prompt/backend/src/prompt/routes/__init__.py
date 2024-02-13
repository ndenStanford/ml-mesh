"""Init."""

# Source
from src.prompt.routes.v1 import router as v1_router
from src.prompt.routes.v2 import router as v2_router


__all__ = ["v1_router", "v2_router"]
