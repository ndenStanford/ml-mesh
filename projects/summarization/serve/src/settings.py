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

    PROMPT_DICT = {
        "en": {
            "alias": "english-summarization-prompt",
            "template": "Give an abstractive summary while retaining important \
                        quotes of speech in less than {word_num} words: \n {content} \n",
        },
        "fr": {
            "alias": "french-summarization-prompt",
            "template": "Donner un résumé abstrait tout en gardant l'importance \
                        citations de discours en moins de {word_num} mots: \n {content} \n",
        },
    }


settings = Settings()
