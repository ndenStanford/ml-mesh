"""Functional."""

# Standard Library
from typing import Dict

# 3rd party libraries
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# Internal libraries
from onclusiveml.core.retry import retry
from onclusiveml.llms.prompt_validator import PromptInjectionfield_validator

# Source
from src.extensions.redis import redis
from src.model.tables import LanguageModel
from src.prompt.tables import PromptTemplate
from src.settings import get_settings


settings = get_settings()
field_validator = PromptInjectionfield_validator()


@retry(tries=settings.LLM_CALL_RETRY_COUNT)
@redis.cache(ttl=settings.REDIS_TTL_SECONDS)
def generate_from_prompt_template(
    prompt_alias: str, model_alias: str, **kwargs
) -> Dict[str, str]:
    """Generates chat message from input prompt and model."""
    # get langchain objects
    prompt = PromptTemplate.get(prompt_alias)
    llm = LanguageModel.get(model_alias)
    # setting output parser
    prompt.fields = kwargs.get("output")

    chain = prompt.as_langchain() | llm.as_langchain() | prompt.output_parser

    inputs = kwargs.get("input", dict())
    inputs.update({"format_instructions": prompt.format_instructions})

    if settings.VALIDATE_PROMPT_INJECTION:
        validate_input = prompt.as_langchain().messages[0].prompt.template
        validate_input = validate_input.format(**inputs)
        field_validator.validate_prompt(validate_input)

    return chain.invoke(inputs)


@retry(tries=settings.LLM_CALL_RETRY_COUNT)
@redis.cache(ttl=settings.REDIS_TTL_SECONDS)
def generate_from_prompt(prompt: str, model_alias: str) -> Dict[str, str]:
    """Generates chat message from input prompt and model."""
    if settings.VALIDATE_PROMPT_INJECTION:
        field_validator.validate_prompt(prompt)
    llm = LanguageModel.get(model_alias).as_langchain()
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

    if settings.VALIDATE_PROMPT_INJECTION:
        validate_input = prompt.as_langchain().messages[0].prompt.template
        validate_input = validate_input.format(**inputs)
        field_validator.validate_prompt(validate_input)

    return chain.invoke(inputs)
