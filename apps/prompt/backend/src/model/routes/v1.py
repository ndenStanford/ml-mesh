"""Model."""

# 3rd party libraries
from fastapi import APIRouter, HTTPException, status

# Internal libraries
from onclusiveml.core.logging import get_default_logger

# Source
from src.model.schemas import ModelListSchema, ModelSchema
from src.model.tables import ModelTable


logger = get_default_logger(__name__)


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
        return ModelSchema.get(model_name)
    except ModelTable.DoesNotExist as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{str(e)} - (model_name={str(model_name)})",
        )
