"""Init."""

__all__ = ["health_router", "gpt3_router"]

from src.routes.health import router as health_router
from src.routes.gpt3_summarize import router as gpt3_router
