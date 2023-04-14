"""Model."""

# 3rd party libraries
from fastapi import APIRouter, HTTPException, Security, status

# Internal libraries
from onclusiveml.core.logging import get_default_logger

# Source
from src.helpers import get_api_key
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
    dependencies=[Security(get_api_key)],
)
def get_models():
    """List models."""
    return {"models": ModelSchema.get()}  # NOTE: Pagination is not needed here (yet)


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=ModelSchema,
    dependencies=[Security(get_api_key)],
)
def get_model(id: str):
    """Retrieves model via id.

    Args:
        id (str): model id
    """
    try:
        return ModelSchema.get(id)
    except ModelTable.DoesNotExist as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{str(e)} - (id={str(id)})"
        )


# @router.post(
#     "", status_code=status.HTTP_201_CREATED, dependencies=[Security(get_api_key)]
# )
# def create_model(model_name: str):
#     """Creates model.

#     Args:
#         model_name (str): model name.
#     """
#     model = ModelSchema(model_name=model_name)
#     return model.save()


# @router.put(
#     "/{id}", status_code=status.HTTP_200_OK, dependencies=[Security(get_api_key)]
# )
# def update_model(id: str, model_name: str):
#     """Updates model.

#     Args:
#         id (str): model id
#         model_name (str): model name.
#     """
#     model = ModelSchema.get(id)
#     model.update(model_name=model_name)
#     return ModelSchema.get(id)


# @router.delete(
#     "/{id}", status_code=status.HTTP_200_OK, dependencies=[Security(get_api_key)]
# )
# def delete_model(id: str):
#     """Deletes model from database.

#     Args:
#         id (str): model id

#     Raises:
#         HTTPException.DoesNotExist if id is not found in table.
#     """
#     try:
#         model = ModelTable.get(id)
#         model.delete()
#         return "deleted"
#     except ModelTable.DoesNotExist as e:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail=f"{str(e)} - (id={str(id)})"
#         )
