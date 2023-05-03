"""Init."""

__all__ = ["router"]

# 3rd party libraries
from fastapi import APIRouter

# Source
from src.routes.v1.entity_linking import router as entity_linking_router
from src.routes.v1.readiness import router as readiness_router


router = APIRouter(
    prefix="/v1",
)

router.include_router(entity_linking_router)
router.include_router(readiness_router)
