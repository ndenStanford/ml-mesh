"""App."""

from onclusiveml.core.logger import get_default_logger
from src.routes import health_router, keybert_router
from src.settings import settings
from src._init import init

from fastapi import FastAPI


logger = get_default_logger(__name__)


def create_app():
    """Creates FastAPI app."""

    logger.debug("Initialising application...")

    app = FastAPI(name=settings.API_NAME, description=settings.API_DESCRIPTION)

    logger.debug("Adding routers...")

    app.include_router(health_router)
    app.include_router(keybert_router)

    logger.debug("Downloading model artefacts...")

    app = init(app)

    return app


app = create_app()
