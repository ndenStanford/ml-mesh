"""Language model parameters."""

# Standard Library
from typing import Optional, Type

# Internal libraries
from onclusiveml.core.base import OnclusiveFrozenSchema

# Source
from src.settings import get_settings


settings = get_settings()


class LanguageModelParameters(OnclusiveFrozenSchema):
    """Language Model Parameters."""

    max_tokens: Optional[int] = settings.DEFAULT_MAX_TOKENS
    temperature: Optional[float] = settings.DEFAULT_TEMPERATURE
    response_format: Optional[Dict] = settings.DEFAULT_RESPONSE_FORMAT
    seed: Optional[int] = settings.DEFAULT_SEED

    @validator("max_tokens")
    def validate_max_tokens(cls, value, values):
        """Validates the maximum tokens parameter.

        Args:
            value (int): The max_tokens value to be validated
            values (dict): The values of the other fields in the model

        Raises:
            PromptInvalidParameters: If the max tokens value is an empty string
            PromptTokenExceedModel: If the max tokens value exceeds the model's limit

        Returns:
            int: The validated max tokens value
        """
        # If max tokens is None then raise exception
        if value in [""]:
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
        """Validates the temperature parameter.

        Args:
            value (float): The temperature value to be validated.

        Raises:
            PromptInvalidParameters: If the temperature value is an empty string
            PromptOutsideTempLimit: If the temperature value is outside the valid range
        """
        # Reject None
        if value is None or value in [""]:
            raise PromptInvalidParameters(param_name="temperature", param=value)
        # check if temperature is between 0 and 1
        if not (0.0 <= value <= 1.0):
            raise PromptOutsideTempLimit()
        return value
