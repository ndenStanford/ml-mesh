"""Functional."""

# Standard Library
from typing import Dict

# 3rd party libraries
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.schema.output_parser import StrOutputParser

# Internal libraries
from onclusiveml.core.retry import retry
from onclusiveml.llms.json_builder import build_json

# Source
from src.extensions.redis import redis
from src.model.tables import LanguageModel
from src.prompt.exceptions import PromptFieldsMissing, StrOutputParserTypeError
from src.prompt.tables import PromptTemplate
from src.settings import get_settings
from src.worker import celery_app


settings = get_settings()


@celery_app.task(
    default_retry_delay=settings.CELERY_RETRY_DELAY,
    max_retries=settings.CELERY_MAX_RETRY_COUNTS,
)
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
    # Check if str_output_parser flag is correctly set and validate fields
    str_output_parser = kwargs.get("str_output_parser", False)
    if not isinstance(str_output_parser, bool):
        raise StrOutputParserTypeError
    # ensure prompt fields are populated in order to run json builder functions
    if str_output_parser and prompt.fields is None:
        raise PromptFieldsMissing

    chain = (
        prompt.as_langchain()
        | llm.as_langchain(model_parameters=model_parameters)
        | prompt.output_parser
    )
    inputs = kwargs.get("input", dict())
    inputs.update({"format_instructions": prompt.format_instructions})
    try:
        result = chain.invoke(inputs)
    except Exception as e:
        if str_output_parser and prompt.fields:
            chain = (
                prompt.as_langchain()
                | llm.as_langchain(model_parameters=model_parameters)
                | StrOutputParser()
            )
            result = chain.invoke(inputs)
            return build_json(result, prompt.fields.keys())
        # else raise error
        else:
            raise e

    return result


@celery_app.task(
    default_retry_delay=settings.CELERY_RETRY_DELAY,
    max_retries=settings.CELERY_MAX_RETRY_COUNTS,
)
@retry(tries=settings.LLM_CALL_RETRY_COUNT)
@redis.cache(ttl=settings.REDIS_TTL_SECONDS)
def generate_from_prompt(
    prompt: str, model_alias: str, model_parameters: Dict = None
) -> Dict[str, str]:
    """Generates chat message from input prompt and model."""
    llm = LanguageModel.get(model_alias).as_langchain(model_parameters=model_parameters)
    conversation = ConversationChain(llm=llm, memory=ConversationBufferMemory())
    return conversation.predict(input=prompt)


@celery_app.task(
    default_retry_delay=settings.CELERY_RETRY_DELAY,
    max_retries=settings.CELERY_MAX_RETRY_COUNTS,
)
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
