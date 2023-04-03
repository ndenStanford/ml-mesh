"""Init."""

__all__ = ["router"]

# 3rd party libraries
from fastapi import APIRouter

# Source
from src.routes.v1.keywords import router as keywords_router


router = APIRouter(
    prefix="/v1",
)

router.include_router(keywords_router)
