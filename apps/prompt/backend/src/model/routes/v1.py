"""Model."""

# 3rd party libraries
from fastapi import APIRouter, HTTPException, status

# Source
from src.model.exceptions import ModelNotFound
from src.model.schemas import ModelListSchema, ModelSchema


router = APIRouter(
    prefix="/v1/models",
)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ModelListSchema,
)
def get_models():
    """List models."""
    return {"models": ModelSchema.get()}  # NOTE: Pagination is not needed here (yet)


@router.get(
    "/{model_name}",
    status_code=status.HTTP_200_OK,
    response_model=ModelSchema,
)
def get_model(model_name: str):
    """Retrieves model via model name.

    Args:
        model_name (str): model name
    """
    try:
        return ModelSchema.get(model_name, raises_if_not_found=True)
    except ModelNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
