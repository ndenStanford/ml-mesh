"""Text generation from prompt."""

# 3rd party libraries
import openai

# Internal libraries
from onclusiveml.core.logging import get_default_logger
from onclusiveml.core.retry import retry

# Source
from src.extensions.redis import cache
from src.model.constants import ModelEnum
from src.settings import get_settings


settings = get_settings()

logger = get_default_logger(__name__)


@retry(tries=2)
@cache.cache(ttl=settings.REDIS_TTL_SECONDS)
def generate_text(
    prompt: str, model_name: str, max_tokens: int, temperature: float
) -> str:
    """Sends request to generate text."""
    logger.info("Calling openai API....")

    openai.api_key = settings.OPENAI_API_KEY
    # Response based on what model we use
    if (
        model_name == ModelEnum.GPT3_5.value
        or model_name == ModelEnum.GPT4.value  # noqa: W503
        or model_name == ModelEnum.DAVINCI.value  # noqa: W503
        or model_name == ModelEnum.CURIE.value  # noqa: W503
    ):
        if model_name == "gpt-3.5-turbo" or model_name == "gpt-4":
            response = openai.ChatCompletion.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return response["choices"][0]["message"]["content"]
        else:
            response = openai.Completion.create(
                model=model_name,
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return response["choices"][0]["text"]
    else:
        return "Model is unknown or not supported"
