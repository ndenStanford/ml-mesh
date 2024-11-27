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
from src.generated.tables import Generated
from src.model.tables import LanguageModel
from src.prompt.constants import GENERATED, CeleryStatusTypes
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
    generated_id = kwargs.get("generated_id", None)

    if generated_id is not None:
        Generated.get(generated_id).update_status(CeleryStatusTypes.STARTED)

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
        if generated_id is not None:
            generation = {GENERATED: result} if isinstance(result, str) else result
            Generated.get(generated_id).update_status(
                CeleryStatusTypes.SUCCESS, generation
            )
    except Exception as e:
        try:
            if str_output_parser and prompt.fields:
                chain = (
                    prompt.as_langchain()
                    | llm.as_langchain(model_parameters=model_parameters)
                    | StrOutputParser()
                )
                result = build_json(chain.invoke(inputs), prompt.fields.keys())
            elif generated_id is not None:
                Generated.get(generated_id).update_status(
                    CeleryStatusTypes.FAILURE, None, str(e)
                )
                raise e
            else:
                raise e
        except Exception as e:
            if generated_id is not None:
                Generated.get(generated_id).update_status(
                    CeleryStatusTypes.FAILURE, None, str(e)
                )
            raise e

    return result


@celery_app.task(
    default_retry_delay=settings.CELERY_RETRY_DELAY,
    max_retries=settings.CELERY_MAX_RETRY_COUNTS,
)
@retry(tries=settings.LLM_CALL_RETRY_COUNT)
@redis.cache(ttl=settings.REDIS_TTL_SECONDS)
def generate_from_prompt(
    prompt: str, model_alias: str, model_parameters: Dict = None, generated_id=None
) -> Dict[str, str]:
    """Generates chat message from input prompt and model."""
    if generated_id is not None:
        Generated.get(generated_id).update_status(CeleryStatusTypes.STARTED)

    llm = LanguageModel.get(model_alias).as_langchain(model_parameters=model_parameters)
    conversation = ConversationChain(llm=llm, memory=ConversationBufferMemory())

    if generated_id is not None:
        try:
            result = conversation.predict(input=prompt)
            generation = {GENERATED: result} if isinstance(result, str) else result
            Generated.get(generated_id).update_status(
                CeleryStatusTypes.SUCCESS, generation
            )
        except Exception as e:
            Generated.get(generated_id).update_status(
                CeleryStatusTypes.FAILURE, None, str(e)
            )
            raise e
    else:
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
    generated_id = kwargs.get("generated_id", None)

    if generated_id is not None:
        Generated.get(generated_id).update_status(CeleryStatusTypes.STARTED)

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

    if generated_id is not None:
        try:
            result = chain.invoke(inputs)
            generation = {GENERATED: result} if isinstance(result, str) else result
            Generated.get(generated_id).update_status(
                CeleryStatusTypes.SUCCESS, generation
            )
        except Exception as e:
            Generated.get(generated_id).update_status(
                CeleryStatusTypes.FAILURE, None, str(e)
            )
            raise e
    else:
        return chain.invoke(inputs)
