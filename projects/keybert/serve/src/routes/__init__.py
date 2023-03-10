"""Init."""

__all__ = ["health_router", "keybert_router"]

from src.routes.health import router as health_router
from src.routes.keybert import router as keybert_router
