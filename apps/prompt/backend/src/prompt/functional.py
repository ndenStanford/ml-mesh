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


@retry(
    tries=settings.LLM_CALL_RETRY_COUNT,
    delay=settings.LLM_CALL_RETRY_DELAY,
    backoff=settings.LLM_CALL_RETRY_BACKOFF,
    max_delay=settings.LLM_CALL_RETRY_MAX_DELAY,
)
@redis.cache(ttl=settings.REDIS_TTL_SECONDS)
def generate_from_prompt_template(
    prompt_alias: str, model_alias: str, **kwargs
) -> Dict[str, str]:
    """Generates chat message from input prompt and model."""
    # get langchain objects
    model_parameters = kwargs.get("model_parameters", None)
    prompt = PromptTemplate.get(prompt_alias)
    llm = LanguageModel.get(model_alias)
    # setting output parser
    prompt.fields = kwargs.get("output")

    chain = (
        prompt.as_langchain()
        | llm.as_langchain(model_parameters=model_parameters)
        | prompt.output_parser
    )

    inputs = kwargs.get("input", dict())
    inputs.update({"format_instructions": prompt.format_instructions})

    return chain.invoke(inputs)


@retry(tries=settings.LLM_CALL_RETRY_COUNT)
@redis.cache(ttl=settings.REDIS_TTL_SECONDS)
def generate_from_prompt(
    prompt: str, model_alias: str, model_parameters: Dict = None
) -> Dict[str, str]:
    """Generates chat message from input prompt and model."""
    llm = LanguageModel.get(model_alias).as_langchain(model_parameters=model_parameters)
    conversation = ConversationChain(llm=llm, memory=ConversationBufferMemory())
    return conversation.predict(input=prompt)


@retry(tries=settings.LLM_CALL_RETRY_COUNT)
@redis.cache(ttl=settings.REDIS_TTL_SECONDS)
def generate_from_default_model(prompt_alias: str, **kwargs) -> Dict[str, str]:
    """Generates chat message from input prompt alias and default model."""
    # get langchain objects
    prompt = PromptTemplate.get(prompt_alias)

    model_alias = settings.DEFAULT_MODELS.get(
        prompt_alias, settings.DEFAULT_MODELS["default"]
    )

    llm = LanguageModel.get(model_alias)
    # setting output parser
    prompt.fields = kwargs.get("output")

    chain = prompt.as_langchain() | llm.as_langchain() | prompt.output_parser

    inputs = kwargs.get("input", dict())
    inputs.update({"format_instructions": prompt.format_instructions})

    return chain.invoke(inputs)
