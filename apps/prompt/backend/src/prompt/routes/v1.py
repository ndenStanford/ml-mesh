"""Prompt."""

# Standard Library
import json
from typing import Any, Dict

# 3rd party libraries
from fastapi import APIRouter, HTTPException, status
from slugify import slugify

# Internal libraries
from onclusiveml.core.logging import get_default_logger

# Source
from src.model.constants import ModelEnum
from src.model.schemas import ModelSchema
from src.prompt.exceptions import DeletionProtectedPrompt, PromptNotFound
from src.prompt.generate import generate_text
from src.prompt.schemas import (
    PromptTemplateListSchema,
    PromptTemplateOutputSchema,
    PromptTemplateSchema,
)
from src.settings import get_settings


settings = get_settings()


logger = get_default_logger(__name__)


router = APIRouter(
    prefix="/v1/prompts",
)


@router.get("", status_code=status.HTTP_200_OK, response_model=PromptTemplateListSchema)
def get_prompts():
    """List prompts."""
    return {
        "prompts": PromptTemplateOutputSchema.from_template_schema(
            PromptTemplateSchema.get()
        )  # NOTE: Pagination is not needed here (yet)
    }


@router.get(
    "/{alias}",
    status_code=status.HTTP_200_OK,
    response_model=PromptTemplateOutputSchema,
)
def get_prompt(alias: str):
    """Retrieves prompt via alias.

    Args:
        alias (str): alias
    """
    try:
        prompt = PromptTemplateSchema.get(alias, raises_if_not_found=True)
    except PromptNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    return PromptTemplateOutputSchema.from_template_schema(prompt)[0]


@router.post("", status_code=status.HTTP_201_CREATED)
def create_prompt(template: str, alias: str):
    """Creates prompt.

    Args:
        template (str): prompt template text.
        alias (str): alias for template.
    """
    alias = slugify(alias)
    prompt = PromptTemplateSchema.get(alias)
    # if prompt does exist, create a new version
    # otherwise create a new prompt with version 0.
    if not prompt:
        return PromptTemplateSchema(template=template, alias=alias).save()

    prompt = prompt[0]
    if prompt.template == template:
        # if no change in the template return the current version
        return prompt
    return prompt.update(template=template)


@router.put("/{alias}", status_code=status.HTTP_200_OK)
def update_prompt(alias: str, template: str):
    """Updates latest version of a prompt.

    Args:
        alias (str): alias
        template (str): prompt template text.
    """
    try:
        prompt = PromptTemplateSchema.get(alias, raises_if_not_found=True)
    except PromptNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    prompt = prompt[0]

    if not prompt.template == template:
        prompt.update(template=template)
    return PromptTemplateSchema.get(alias)[0]


@router.delete("/{alias}", status_code=status.HTTP_200_OK)
def delete_prompt(alias: str):
    """Deletes prompt from database.

    Args:
        alias (str): prompt alias

    Raises:
        HTTPException.DoesNotExist if alias is not found in table.
    """
    try:
        PromptTemplateSchema(alias=alias, template="").delete()
        return "deleted"
    except PromptNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except DeletionProtectedPrompt as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )


@router.post("/{alias}/generate", status_code=status.HTTP_200_OK)
def generate(alias: str, values: Dict[str, Any]):
    """Generates text using a prompt template.

    Args:
        alias (str): prompt alias
        values (Dict[str, Any]): values to fill in template.
    """
    prompt_template: PromptTemplateSchema = PromptTemplateSchema.get(alias)[0]
    prompt = prompt_template.prompt(**values)
    return {
        "prompt": prompt,
        "generated": generate_text(
            prompt,
            ModelEnum.GPT3_5.value,
            settings.OPENAI_MAX_TOKENS,
            settings.OPENAI_TEMPERATURE,
        ),
    }


@router.post("/{alias}/generate/model/{model_name}", status_code=status.HTTP_200_OK)
def generate_with_diff_model(alias: str, model_name: str, values: Dict[str, Any]):
    """Generates text using a prompt template.

    Args:
        alias (str): prompt alias
        model_name (str): model name
        values (Dict[str, Any]): values to fill in template.
    """
    prompt_template: PromptTemplateSchema = PromptTemplateSchema.get(alias)[0]
    prompt = prompt_template.prompt(**values)
    model = ModelSchema.get(model_name)
    return {
        "prompt": prompt,
        "generated": generate_text(
            prompt,
            model.model_name,
            int(json.loads(model.parameters)["max_tokens"]),
            float(json.loads(model.parameters)["temperature"]),
        ),
    }


@router.get("/generate/{prompt}", status_code=status.HTTP_200_OK)
def generate_test(prompt: str):
    """Retrieves prompt via id.
    Args:
        prompt (str): prompt input from chat
    """
    return {
        "generated": generate_text(
            prompt,
            ModelEnum.GPT3_5.value,
            settings.OPENAI_MAX_TOKENS,
            settings.OPENAI_TEMPERATURE,
        ),
    }


@router.get("/generate/{prompt}/model/{model_name}", status_code=status.HTTP_200_OK)
def generate_test_with_diff_model(prompt: str, model_name: str):
    """Retrieves prompt via id.
    Args:
        prompt (str): prompt input from chat
        model_name (str): model name
    """
    model = ModelSchema.get(model_name)
    return {
        "generated": generate_text(
            prompt,
            model.model_name,
            int(json.loads(model.parameters)["max_tokens"]),
            float(json.loads(model.parameters)["temperature"]),
        ),
    }
