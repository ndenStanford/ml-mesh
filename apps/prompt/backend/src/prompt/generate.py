"""Text generation from prompt."""

# 3rd party libraries
import openai
import redis
from redis_cache import RedisCache

# Internal libraries
from onclusiveml.core.retry import retry

# Source
from src.model.constants import ModelEnum
from src.settings import get_settings


settings = get_settings()

client = redis.from_url(settings.REDIS_CONNECTION_STRING)
cache = RedisCache(redis_client=client)


@retry(tries=2)
@cache.cache()
def generate_text(
    prompt: str, model_name: str, max_tokens: int, temperature: float
) -> str:
    """Sends request to generate text."""

    openai.api_key = settings.OPENAI_API_KEY
    # Response based on what model we use
    if (
        model_name == ModelEnum.GPT3_5.value
        or model_name == ModelEnum.GPT4.value  # noqa: W503
        or model_name == ModelEnum.DAVINCI.value  # noqa: W503
        or model_name == ModelEnum.CURIE.value  # noqa: W503
    ):

        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response["choices"][0]["message"]["content"]
    else:
        return "Sorry, the backend for this model is in development"
