# Standard Library
from typing import Optional

# 3rd party libraries
from pydantic import BaseModel, validator

# Source
from src.model.constants import ModelEnum
from src.prompt.exceptions import (
    PromptModelUnsupported,
    PromptOutsideTempLimit,
    PromptTokenExceedModel,
)
from src.settings import get_settings


settings = get_settings()


class Parameters(BaseModel):
    model_name: Optional[str] = ModelEnum.GPT3_5.value
    max_tokens: Optional[int] = settings.OPENAI_MAX_TOKENS
    temperature: Optional[float] = settings.OPENAI_TEMPERATURE

    @classmethod
    def from_dict(cls, params_dict):
        return cls(**params_dict)

    @validator("model_name")
    def validate_model_name(cls, value):
        # Reject None
        if value is None:
            raise PromptNoneParameters(param=value)
        # if model is not supported then reject
        elif value not in ModelEnum.list():
            raise PromptModelUnsupported(model=value)
        return value

    @validator("max_tokens")
    def validate_max_tokens(cls, value, values):
        # If max tokens is None then raise exception
        if value is None:
            raise PromptNoneParameters(param=value)
        # if max tokens is over the limit or less than 0 then raise exception
        elif values.get("model_name") == settings.LIST_OF_MODELS["1"][0] and (
            value > int(settings.LIST_OF_MODELS["1"][2]) or value <= 0
        ):
            raise PromptTokenExceedModel(
                model=values.get("model_name"),
                max_token_length=settings.LIST_OF_MODELS["1"][2],
            )
        elif values.get("model_name") == settings.LIST_OF_MODELS["2"][0] and (
            value > int(settings.LIST_OF_MODELS["2"][2]) or value <= 0
        ):
            raise PromptTokenExceedModel(
                model=values.get("model_name"),
                max_token_length=settings.LIST_OF_MODELS["2"][2],
            )

        return value

    @validator("temperature")
    def validate_temperature(cls, value):
        # Reject None
        if value is None:
            raise PromptNoneParameters(param=value)
        # check if temperature is between 0 and 1
        if not (0.0 <= value <= 1.0):
            raise PromptOutsideTempLimit()
        return value
