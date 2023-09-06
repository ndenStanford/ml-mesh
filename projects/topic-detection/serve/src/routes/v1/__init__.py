"""Init."""

__all__ = ["router"]

# 3rd party libraries
from fastapi import APIRouter

# Source
from src.routes.v1.gpt_topic import router as topic_router


router = APIRouter(
    prefix="/v1",
)

router.include_router(topic_router)
