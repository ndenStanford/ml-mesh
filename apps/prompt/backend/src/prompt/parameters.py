"""Parameters."""


# Standard Library
from typing import Optional

# 3rd party libraries
from pydantic import BaseModel, validator

# Source
from src.model.constants import ModelEnum
from src.prompt.exceptions import (
    PromptInvalidParameters,
    PromptModelUnsupported,
    PromptOutsideTempLimit,
    PromptTokenExceedModel,
)
from src.settings import get_settings


settings = get_settings()


class Parameters(BaseModel):
    """Represents the parameters for the prompt generation.

    Attributes:
        model_name (Optional[str]): The name of the model to be used. Defaults to
            ModelEnum.GPT3_5.value
        max_tokens (Optional[int]): The max number of tokens in the generated prompt. Defaults
            to settings.OPENAI_MAX_TOKENS
        temperature (Optional[float]): The temperature for controlling the randomness in the
            output. Defaults to settings.OPENAI_TEMPERATURE
    """

    model_name: Optional[str] = ModelEnum.GPT3_5.value
    max_tokens: Optional[int] = settings.OPENAI_MAX_TOKENS
    temperature: Optional[float] = settings.OPENAI_TEMPERATURE

    @classmethod
    def from_dict(cls, params_dict):
        """
        Creates a Parameters instance from a dictionary

        Args:
            value (str): The model name to be validated

        Returns:
            Parameters: An instance of the Parameters class
        """
        return cls(**params_dict)

    @validator("model_name")
    def validate_model_name(cls, value):
        """
        Validates the model name

        Args:
            value (str): The model name to be validated

        Raises:
            PromptInvalidParameters: If the model name is non or an empty string
            PromptModelUnsupported: If the model name is not supported

        Returns:
            str: The validated model name
        """

        # Reject None
        if value is None or value in [""]:
            raise PromptInvalidParameters(param_name="model_name", param=value)
        # if model is not supported then reject
        elif value not in ModelEnum.list():
            raise PromptModelUnsupported(model=value)
        return value

    @validator("max_tokens")
    def validate_max_tokens(cls, value, values):
        """
        Validates the maximum tokens parameter.

        Args:
            value (int): The max_tokens value to be validated
            values (dict): The values of the other fields in the model

        Raises:
            PromptInvalidParameters: If the max tokens value is None or an empty string
            PromptTokenExceedModel: If the max tokens value exceeds the model's limit

        Returns:
            int: The validated max tokens value
        """

        # If max tokens is None then raise exception
        if value is None or value in [""]:
            raise PromptInvalidParameters(param_name="max_tokens", param=value)
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
        """
        Validates the temperature parameter.

        Args:
            value (float): The temperature value to be validated.

        Raises:
            PromptInvalidParameters: If the temperature value is None or an empty string
            PromptOutsideTempLimit: If the temperature value is outside the valid range
        """
        # Reject None
        if value is None or value in [""]:
            raise PromptInvalidParameters(param_name="temperature", param=value)
        # check if temperature is between 0 and 1
        if not (0.0 <= value <= 1.0):
            raise PromptOutsideTempLimit()
        return value
