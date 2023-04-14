"""Health endpoint"""

# 3rd party libraries
from fastapi import APIRouter, status


router = APIRouter()


@router.get("/health", status_code=status.HTTP_200_OK)
async def health() -> str:
    return "OK"
