"""Init."""

__all__ = ["router"]

# 3rd party libraries
from fastapi import APIRouter

# Source
from src.routes.v1.summarization import router as summarization_router


router = APIRouter(
    prefix="/v1",
)

router.include_router(summarization_router)
