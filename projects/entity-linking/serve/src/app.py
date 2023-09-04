"""App."""

# 3rd party libraries
from fastapi import FastAPI

# Internal libraries
from onclusiveml.core.logging import get_default_logger

# Source
from src._init import init
from src.routes import entity_linking_router, health_router, readiness_router
from src.settings import settings


logger = get_default_logger(__name__)


def create_app() -> FastAPI:
    """Creates FastAPI app."""
    logger.debug("Initializing application...")

    app = FastAPI(
        name=settings.API_NAME,
        description=settings.API_DESCRIPTION,
        docs_url=settings.DOCS_URL,
        on_startup=[init],
    )

    logger.debug("Adding routers...")

    app.include_router(health_router)
    app.include_router(entity_linking_router)
    app.include_router(readiness_router)

    return app


app = create_app()
