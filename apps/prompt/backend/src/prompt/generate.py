"""Text generation from prompt."""

# 3rd party libraries
import openai

# Internal libraries
from onclusiveml.core.logging import get_default_logger
from onclusiveml.core.retry import retry

# Source
from src.extensions.redis import cache
from src.model.constants import ModelEnumChat, ModelEnumCompletions
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
    if model_name in ModelEnumChat.list() or model_name in ModelEnumCompletions.list():
        if model_name in ModelEnumChat.list():
            response = openai.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return response.choices[0].message.content
        else:
            response = openai.completions.create(
                model=model_name,
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return response.choices[0].text
    else:
        return "Model is unknown or not supported"
