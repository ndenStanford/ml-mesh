"""Endpoints."""

# 3rd party libraries
from fastapi import APIRouter, status

from src.prompt.routes import v1_router as prompt_v1_router


health_router = APIRouter()
api_router = APIRouter(prefix="/api")

@health_router.get("/health", status_code=status.HTTP_200_OK)
async def health() -> str:
    """Health endpoint."""
    return "OK"


api_router.include_router(prompt_v1_router)
