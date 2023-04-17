"""Text generation from prompt."""

# 3rd party libraries
import openai

# Source
from src.model.model_enum import ModelEnum
from src.settings import get_settings


settings = get_settings()


def generate_text(prompt: str, model_name: str) -> str:
    """Sends request to generate text."""

    openai.api_key = settings.OPENAI_API_KEY
    # Response based on what model we use
    if (
        model_name == ModelEnum.GPT3_5.value
        or model_name == ModelEnum.DAVINCI.value  # noqa: W503
        or model_name == ModelEnum.CURIE.value  # noqa: W503
    ):

        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=settings.OPENAI_MAX_TOKENS,
            temperature=settings.OPENAI_TEMPERATURE,
        )
        return response["choices"][0]["message"]["content"]
    else:
        return "Sorry, the backend for this model is in development"
