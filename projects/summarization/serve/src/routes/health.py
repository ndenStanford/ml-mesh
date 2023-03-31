"""Health endpoint"""

# Third party libs
from fastapi import APIRouter, status


router = APIRouter()


@router.get("/health", status_code=status.HTTP_200_OK)
async def health() -> str:
    return "OK"
