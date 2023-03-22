"""Init."""

__all__ = ["health_router", "summarization_router"]

from src.routes.health import router as health_router
from src.routes.summarization import router as summarization_router
