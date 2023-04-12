"""Keybert predictions."""

# 3rd party libraries
from fastapi import APIRouter, HTTPException, Security, status

# Internal libraries
from onclusiveml.core.logging import get_default_logger

# Source
from src.helpers import get_api_key
from src.model.schemas import ModelTemplateListSchema, ModelTemplateSchema
from src.model.tables import ModelTemplateTable


logger = get_default_logger(__name__)


router = APIRouter(
    prefix="/v1/models",
)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ModelTemplateListSchema,
    dependencies=[Security(get_api_key)],
)
def get_models():
    """List models."""
    return {
        "models": ModelTemplateSchema.get()  # NOTE: Pagination is not needed here (yet)
    }


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=ModelTemplateSchema,
    dependencies=[Security(get_api_key)],
)
def get_model(id: str):
    """Retrieves model via id.

    Args:
        id (str): model id
    """
    try:
        return ModelTemplateSchema.get(id)
    except ModelTemplateTable.DoesNotExist as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{str(e)} - (id={str(id)})"
        )


@router.post(
    "", status_code=status.HTTP_201_CREATED, dependencies=[Security(get_api_key)]
)
def create_model(template: str):
    """Creates model.

    Args:
        template (str): model template text.
    """
    model = ModelTemplateSchema(template=template)
    return model.save()


@router.put(
    "/{id}", status_code=status.HTTP_200_OK, dependencies=[Security(get_api_key)]
)
def update_model(id: str, template: str):
    """Updates model.

    Args:
        id (str): model id
        template (str): model template text.
    """
    model = ModelTemplateSchema.get(id)
    model.update(template=template)
    return ModelTemplateSchema.get(id)


@router.delete(
    "/{id}", status_code=status.HTTP_200_OK, dependencies=[Security(get_api_key)]
)
def delete_model(id: str):
    """Deletes model from database.

    Args:
        id (str): model id

    Raises:
        HTTPException.DoesNotExist if id is not found in table.
    """
    try:
        model = ModelTemplateTable.get(id)
        model.delete()
        return "deleted"
    except ModelTemplateTable.DoesNotExist as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{str(e)} - (id={str(id)})"
        )
