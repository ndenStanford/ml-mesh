"""App."""

# 3rd party libraries
from fastapi import FastAPI

# Internal libraries
from onclusiveml.core.logging import get_default_logger

# Source
from src.routes import health_router, v1_router
from src.settings import settings


logger = get_default_logger(__name__)


def create_app() -> FastAPI:
    """Creates FastAPI app."""

    logger.debug("Initialising application...")

    app = FastAPI(name=settings.API_NAME, description=settings.API_DESCRIPTION)

    logger.debug("Adding routers...")

    app.include_router(health_router)
    app.include_router(v1_router)

    return app


app = create_app()
