"""Init."""

__all__ = ["health_router"]

# Source
from src.routes.health import router as health_router
from src.routes.v1.entity_linking import router as entity_linking_router
from src.routes.v1.readiness import router as readiness_router
