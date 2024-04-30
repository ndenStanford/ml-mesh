"""Functional."""

# Standard Library
from typing import Dict

# 3rd party libraries
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# Internal libraries
from onclusiveml.core.retry import retry

# Source
from src.extensions.redis import redis
from src.model.tables import LanguageModel
from src.prompt.tables import PromptTemplate
from src.settings import get_settings


settings = get_settings()


@retry(tries=settings.LLM_CALL_RETRY_COUNT)
@redis.cache(ttl=settings.REDIS_TTL_SECONDS)
def generate_from_prompt_template(
    prompt_alias: str, model_alias: str, **kwargs
) -> Dict[str, str]:
    """Generates chat message from input prompt and model."""
    # get langchain objects
    prompt = PromptTemplate.get(prompt_alias).as_langchain()
    llm = LanguageModel.get(model_alias).as_langchain()
    conversation = ConversationChain(llm=llm, memory=ConversationBufferMemory())
    return {
        "prompt": prompt.format(**kwargs),
        "generated": conversation.predict(input=prompt.format(**kwargs)),
    }


@retry(tries=settings.LLM_CALL_RETRY_COUNT)
@redis.cache(ttl=settings.REDIS_TTL_SECONDS)
def generate_from_prompt(
    prompt: str,
    model_alias: str,
) -> Dict[str, str]:
    """Generates chat message from input prompt and model."""
    llm = LanguageModel.get(model_alias).as_langchain()
    conversation = ConversationChain(llm=llm)
    return {"prompt": prompt, "generated": conversation.predict(input=prompt)}
