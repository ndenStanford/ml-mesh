"""Health endpoint"""
# Standard library

# 3rd party libraries
from fastapi import APIRouter, status

# Source
from src.settings import get_settings


settings = get_settings()

router = APIRouter()


@router.get("/health", status_code=status.HTTP_200_OK)
async def health() -> str:
    return "OK"
