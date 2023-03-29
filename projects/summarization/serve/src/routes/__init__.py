"""Init."""

__all__ = ["health_router", "v1_router"]

# Source
from src.routes.health import router as health_router
from src.routes.v1 import router as v1_router
