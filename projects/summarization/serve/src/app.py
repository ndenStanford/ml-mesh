"""App."""

from onclusiveml.core.logger import get_default_logger
from src.routes import health_router, summarization_router
from src.settings import settings

from fastapi import FastAPI


logger = get_default_logger(__name__)


def create_app():
    """Creates FastAPI app."""

    logger.debug("Initialising application...")

    app = FastAPI(name=settings.API_NAME, description=settings.API_DESCRIPTION)

    logger.debug("Adding routers...")

    app.include_router(health_router)
    app.include_router(summarization_router)

    return app


app = create_app()
