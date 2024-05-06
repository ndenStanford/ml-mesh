"""Endpoints."""
# Standard

# 3rd party libraries
import requests
from fastapi import APIRouter, status

# Source
from src.model.routes import router as model_router
from src.project.routes import router as project_router
from src.prompt.routes import router as prompt_router
from src.settings import get_settings


settings = get_settings()


health_router = APIRouter()
api_router = APIRouter(prefix="/api")


@health_router.get("/health", status_code=status.HTTP_200_OK)
async def health() -> str:
    """Health endpoint."""
    if settings.ENVIRONMENT != "dev":
        requests.post(
            "https://uptime.betterstack.com/api/v1/heartbeat/{}".format(
                settings.BETTERSTACK_KEY
            )
        )
    return "OK"


api_router.include_router(model_router)
api_router.include_router(prompt_router)
api_router.include_router(project_router)
