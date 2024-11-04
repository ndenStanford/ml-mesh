"""Functional."""

# Standard Library
from typing import Dict

# 3rd party libraries
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.schema.output_parser import StrOutputParser

# Internal libraries
from onclusiveml.core.retry import retry

# Source
from src.extensions.redis import redis
from src.model.tables import LanguageModel
from src.prompt.json_builder import build_json
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
    # Choose StrOutputParser if str_output_parser is True and prompt fields are defined
    # otherwise, use the default prompt output parser
    str_output_parser = kwargs.get("str_output_parser", False)
    output_parser = (
        StrOutputParser()
        if str_output_parser is True and prompt.fields
        else prompt.output_parser
    )

    chain = (
        prompt.as_langchain()
        | llm.as_langchain(model_parameters=model_parameters)
        | output_parser
    )

    inputs = kwargs.get("input", dict())
    inputs.update({"format_instructions": prompt.format_instructions})
    result = chain.invoke(inputs)
    # If str_output_parser is True and fields are defined, format the output as JSON
    if str_output_parser is True and prompt.fields:
        return build_json(result, prompt.fields.keys())
    return result


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
