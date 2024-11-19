"""Generated."""

# 3rd party libraries
from dyntastic.exceptions import DoesNotExist
from fastapi import APIRouter, HTTPException, status

# Source
from src.generated.exceptions import GeneratedExisting
from src.generated.tables import Generated

router = APIRouter(
    prefix="/v3/generated",
)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_generated(generated: Generated):
    """Creates generated object.

    Args:
        id (str): id for generated object.
    """
    _generated = Generated.safe_get(generated.id)
    # if generated does exist, create it
    if _generated is None:
        try:
            generated.save()
            return generated

        except HTTPException as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(e),
            )
    else:
        e = GeneratedExisting(id=generated.id)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_generated(id: str):
    """Deletes generated from database.

    Args:
        id (str): generated id

    Raises:
        HTTPException.DoesNotExist if id is not found in table.
    """
    try:
        generated = Generated.get(id)
        generated.delete()
        return generated
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Generated {id} not found in database",
        )


@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_generated(id: str):
    """Get generated from database.

    Raises:
        HTTPException.GeneratedNotFound generated id not found in table.
    """
    try:
        return Generated.get(id)
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Generated {id} not found in database",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
