"""Text generation from prompt."""

# TODO: [DS-426] Add model module to manage models and call parameters.

# 3rd party libraries
import openai

# Source
from src.settings import get_settings


settings = get_settings()


def generate_text(prompt: str, model: str) -> str:
    """Sends request to generate text."""

    openai.api_key = settings.OPENAI_API_KEY

    response = openai.ChatCompletion.create(
        model=model,  # "gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=settings.OPENAI_MAX_TOKENS,
        temperature=settings.OPENAI_TEMPERATURE,
    )
    return response["choices"][0]["message"]["content"]
