"""Settings."""

# Standard Library
from typing import Optional

# 3rd party libraries
from pydantic import BaseSettings


class Settings(BaseSettings):
    """API configuration."""

    # Generic settings

    # API name
    API_NAME: str = "Summarization Prediction"

    # API description
    API_DESCRIPTION: str = ""

    # API environment
    ENVIRONMENT: str = "stage"

    # Debug level
    DEBUG: bool = True

    # API runtime
    KUBERNETES_IN_POD: bool = False

    # Logging level
    LOGGING_LEVEL: str = "info"

    # documentation endpoint
    DOCS_URL: Optional[str] = None

    # OpenAI api key
    OPENAI_API_KEY: str = ""

    # Prompt url
    PROMPT_API: str = "http://0.0.0.0:4000"
    PROMPT_API_KEY: str = "1234"

    ENGLISH_SUMMARIZATION_ALIAS = "english-summarization-prompt"

settings = Settings()

import requests 

headers = {'x-api-key': settings.PROMPT_API_KEY}
q = requests.get("{}/api/v1/prompts".format(settings.PROMPT_API), headers = headers)
prompts = eval(q.content)["prompts"]
english_prompt_dict = [prompt for prompt in prompts if prompt["alias"] == settings.ENGLISH_SUMMARIZATION_ALIAS]
english_prompt_id = english_prompt_dict[0]["id"]

q = requests.get("{}/api/v1/prompts/{}".format(settings.PROMPT_API, english_prompt_id), headers = headers)
template = eval(q.content)["template"]
content = "This is a test content"
template