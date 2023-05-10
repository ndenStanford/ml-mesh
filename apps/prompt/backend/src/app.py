"""App."""

# 3rd party libraries
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Internal libraries
from onclusiveml.core.logging import get_default_logger

# Source
from src._init import init
from src.routes import api_router, health_router
from src.settings import get_settings


settings = get_settings()


logger = get_default_logger(__name__)


def create_app(initialize: bool = True) -> FastAPI:
    """Creates FastAPI app."""

    logger.debug("Initializing application...")

    on_startup = []

    if initialize:
        on_startup.append(init)

    app = FastAPI(
        name=settings.API_NAME,
        description=settings.API_DESCRIPTION,
        docs_url=settings.DOCS_URL,
        on_startup=on_startup,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGIN,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )

    logger.debug("Adding routers...")

    app.include_router(health_router)
    app.include_router(api_router)

    return app


app = create_app(settings.INITIALIZE)
