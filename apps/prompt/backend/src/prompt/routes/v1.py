"""Keybert predictions."""

# Standard Library
from typing import Any, Dict

# 3rd party libraries
from fastapi import APIRouter, HTTPException, Security, status

# Internal libraries
from onclusiveml.core.logging import get_default_logger

# Source
from src.helpers import get_api_key
from src.prompt.generate import generate_text
from src.prompt.schemas import PromptTemplateListSchema, PromptTemplateSchema
from src.prompt.tables import PromptTemplateTable


logger = get_default_logger(__name__)


router = APIRouter(
    prefix="/v1/prompts",
)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=PromptTemplateListSchema,
    dependencies=[Security(get_api_key)],
)
def get_prompts():
    """List prompts."""
    return {
        "prompts": PromptTemplateSchema.get()  # NOTE: Pagination is not needed here (yet)
    }


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=PromptTemplateSchema,
    dependencies=[Security(get_api_key)],
)
def get_prompt(id: str):
    """Retrieves prompt via id"""
    try:
        return PromptTemplateSchema.get(id)
    except PromptTemplateTable.DoesNotExist as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{str(e)} - (id={str(id)})"
        )


@router.post(
    "", status_code=status.HTTP_201_CREATED, dependencies=[Security(get_api_key)]
)
def create_prompt(template: str):
    """Creates prompt."""
    prompt = PromptTemplateSchema(template=template)
    return prompt.save()


@router.put(
    "/{id}", status_code=status.HTTP_200_OK, dependencies=[Security(get_api_key)]
)
def update_prompt(id: str, template: str):
    prompt = PromptTemplateSchema.get(id)
    prompt.update(template=template)
    return PromptTemplateSchema.get(id)


@router.delete(
    "/{id}", status_code=status.HTTP_200_OK, dependencies=[Security(get_api_key)]
)
def delete_prompts(id: str):
    try:
        prompt = PromptTemplateTable.get(id)
        prompt.delete()
        return "deleted"
    except PromptTemplateTable.DoesNotExist as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{str(e)} - (id={str(id)})"
        )


@router.post(
    "/{id}/generate",
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_api_key)],
)
def generate(id: str, values: Dict[str, Any]):
    prompt_template = PromptTemplateSchema.get(id)
    return {"generated": generate_text(prompt_template.prompt(**values))}
