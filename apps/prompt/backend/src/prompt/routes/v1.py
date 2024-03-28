"""Prompt."""

# Standard Library
import json
from typing import Any, Dict, Optional

# 3rd party libraries
from fastapi import APIRouter, HTTPException, status
from slugify import slugify

# Source
from src.model.constants import ModelEnumChat
from src.model.exceptions import ModelNotFound
from src.model.schemas import ModelSchema
from src.prompt.chat import PromptChat
from src.prompt.exceptions import (
    DeletionProtectedPrompt,
    PromptInvalidParameters,
    PromptModelUnsupported,
    PromptNotFound,
    PromptOutsideTempLimit,
    PromptTokenExceedModel,
)
from src.prompt.generate import generate_text
from src.prompt.parameters import Parameters
from src.prompt.schemas import (
    PromptInvalidTemplate,
    PromptTemplateListSchema,
    PromptTemplateOutputSchema,
    PromptTemplateSchema,
)
from src.settings import get_settings


settings = get_settings()

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
def create_prompt(template: str, alias: str, parameters: Optional[Dict] = None):
    """Creates prompt.

    Args:
        template (str): prompt template text.
        alias (str): alias for template.
        parameters (Optional[dict]): model and parameters values to be used with prompt
    """
    alias = slugify(alias)
    prompt = PromptTemplateSchema.get(alias)
    # if prompt does exist, create a new version
    # otherwise create a new prompt with version 0.
    if not prompt:
        try:
            if parameters is None or parameters == {}:
                return PromptTemplateSchema(template=template, alias=alias).save()
            else:
                params_instance = Parameters.from_dict(parameters)
                return PromptTemplateSchema(
                    template=template, alias=alias, parameters=params_instance
                ).save()

        except (
            PromptTokenExceedModel,
            PromptOutsideTempLimit,
            PromptModelUnsupported,
            PromptInvalidParameters,
            PromptInvalidTemplate,
        ) as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(e),
            )

    prompt = prompt[0]
    if prompt.template == template:
        # if no change in the template return the current version
        return prompt
    try:
        return prompt.update(template=template, parameters=parameters)
    except (
        PromptTokenExceedModel,
        PromptOutsideTempLimit,
        PromptModelUnsupported,
        PromptInvalidParameters,
        PromptInvalidTemplate,
    ) as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )


@router.put("/{alias}", status_code=status.HTTP_200_OK)
def update_prompt(alias: str, template: str, parameters: Optional[Dict] = None):
    """Updates latest version of a prompt.

    Args:
        alias (str): alias
        template (str): prompt template text.
        parameters (Optional[dict]): model and parameters values to be used with prompt
    """
    try:
        prompt = PromptTemplateSchema.get(alias, raises_if_not_found=True)
    except PromptNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    prompt = prompt[0]

    try:
        if template != prompt.template or parameters is not None or parameters == {}:
            if parameters is not None or parameters == {}:
                params_instance = Parameters.from_dict(parameters)
                if params_instance != prompt.parameters:
                    prompt.update(template=template, parameters=params_instance)
                else:
                    prompt.update(template=template)
            else:
                prompt.update(template=template)
    except (
        PromptTokenExceedModel,
        PromptOutsideTempLimit,
        PromptModelUnsupported,
        PromptInvalidParameters,
        PromptInvalidTemplate,
    ) as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
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
        PromptTemplateSchema(alias=alias, template="prompt to be deleted").delete()
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
    # defaul parameters
    model_name = ModelEnumChat.GPT3_5.value
    max_tokens = settings.OPENAI_MAX_TOKENS
    temperature = settings.OPENAI_TEMPERATURE
    response_format = settings.RESPONSE_FORMAT
    seed = settings.SEED
    # Override if parameters exist
    if prompt_template.parameters is not None:
        model_name = prompt_template.parameters.model_name

        if prompt_template.parameters.max_tokens is None:
            max_tokens = None
        else:
            max_tokens = int(prompt_template.parameters.max_tokens)
        temperature = float(prompt_template.parameters.temperature)
        response_format = prompt_template.parameters.response_format
        seed = prompt_template.parameters.seed
    # if parameters field exists, replace model and parameter values
    return {
        "prompt": prompt,
        "generated": generate_text(
            prompt,
            model_name,
            max_tokens,
            temperature,
            response_format,
            seed,
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
    try:
        prompt_template: PromptTemplateSchema = PromptTemplateSchema.get(
            alias, raises_if_not_found=True
        )[0]
        prompt = prompt_template.prompt(**values)
        model = ModelSchema.get(model_name=model_name, raises_if_not_found=True)
    except ModelNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except PromptNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    return {
        "prompt": prompt,
        "generated": generate_text(
            prompt,
            model.model_name,
            int(json.loads(model.parameters)["max_tokens"]),
            float(json.loads(model.parameters)["temperature"]),
            settings.RESPONSE_FORMAT,
            settings.SEED,
        ),
    }


@router.post("/generate", status_code=status.HTTP_200_OK)
def generate_text_from_chat(values: PromptChat):
    """Retrieves prompt via id.

    Args:
        values (Dict[str, Any]): input from chat
    """
    return {
        "generated": generate_text(
            values.prompt,
            ModelEnumChat.GPT3_5.value,
            settings.OPENAI_MAX_TOKENS,
            settings.OPENAI_TEMPERATURE,
            settings.RESPONSE_FORMAT,
            settings.SEED,
        ),
    }


@router.post("/generate/model/{model_name}", status_code=status.HTTP_200_OK)
def generate_text_from_chat_diff_model(model_name: str, values: PromptChat):
    """Retrieves prompt via id.

    Args:
        values (Dict[str, Any]): input from chat
        model_name (str): model name
    """
    try:
        model = ModelSchema.get(model_name=model_name, raises_if_not_found=True)
    except ModelNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    return {
        "generated": generate_text(
            values.prompt,
            model.model_name,
            int(json.loads(model.parameters)["max_tokens"]),
            float(json.loads(model.parameters)["temperature"]),
            settings.RESPONSE_FORMAT,
            settings.SEED,
        ),
    }
