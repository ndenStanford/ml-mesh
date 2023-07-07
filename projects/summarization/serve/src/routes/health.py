"""Health endpoint"""
# Standard library

# 3rd party libraries
import requests
from fastapi import APIRouter, status

# Source
from src.settings import get_settings


settings = get_settings()

router = APIRouter()


@router.get("/health", status_code=status.HTTP_200_OK)
async def health() -> str:
    """health endpoint"""
    if settings.ENVIRONMENT in ("stage", "prod", "dev"):
        requests.post(
            "https://uptime.betterstack.com/api/v1/heartbeat/{}".format(
                settings.BETTERSTACK_KEY
            )
        )
    return "OK"
