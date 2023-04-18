"""Prompt."""

# Standard Library
import json
from typing import Any, Dict

# 3rd party libraries
from fastapi import APIRouter, HTTPException, Security, status

# Internal libraries
from onclusiveml.core.logging import get_default_logger

# Source
from src.helpers import get_api_key
from src.model.schemas import ModelSchema
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
    """Retrieves prompt via id.

    Args:
        id (str): prompt id
    """
    try:
        return PromptTemplateSchema.get(id)
    except PromptTemplateTable.DoesNotExist as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{str(e)} - (id={str(id)})"
        )


@router.post(
    "", status_code=status.HTTP_201_CREATED, dependencies=[Security(get_api_key)]
)
def create_prompt(template: str, alias: str):
    """Creates prompt.

    Args:
        template (str): prompt template text.
        alias (str): alias for template.
    """
    prompt = PromptTemplateSchema(template=template, alias=alias)
    return prompt.save()


@router.put(
    "/{id}", status_code=status.HTTP_200_OK, dependencies=[Security(get_api_key)]
)
def update_prompt(id: str, template: str):
    """Updates prompt.

    Args:
        id (str): prompt id
        template (str): prompt template text.
    """
    prompt = PromptTemplateSchema.get(id)
    prompt.update(template=template)
    return PromptTemplateSchema.get(id)


@router.delete(
    "/{id}", status_code=status.HTTP_200_OK, dependencies=[Security(get_api_key)]
)
def delete_prompt(id: str):
    """Deletes prompt from database.

    Args:
        id (str): prompt id

    Raises:
        HTTPException.DoesNotExist if id is not found in table.
    """
    try:
        # TODO: for consistency this method should be moved to PromptTemplateSchema
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
    """Generates text using a prompt template.

    Args:
        id (str): prompt id
        values (Dict[str, Any]): values to fill in template.
    """
    prompt_template = PromptTemplateSchema.get(id)
    return {
        "generated": generate_text(
            prompt_template.prompt(**values), "gpt-3.5-turbo", 512, 0.7
        )
    }


@router.post(
    "/{id}/generate/model/{model_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_api_key)],
)
def generate_with_diff_model(id: str, model_id: str, values: Dict[str, Any]):
    """Generates text using a prompt template.

    Args:
        id (str): prompt id
        model_id (str): model id
        values (Dict[str, Any]): values to fill in template.
    """
    prompt_template = PromptTemplateSchema.get(id)
    model = ModelSchema.get(model_id)
    return {
        "generated": generate_text(
            prompt_template.prompt(**values),
            model.model_name,
            int(json.loads(model.parameters)["max_tokens"]),
            float(json.loads(model.parameters)["temperature"]),
        )
    }
