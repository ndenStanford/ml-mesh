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
            "alias": "ml-summarization-english",
            "template": "Give an abstractive summary while retaining important \
                        quotes of speech in less than {desired_length} words: \n {content} \n",
        },
        "fr": {
            "alias": "ml-summarization-french",
            "template": "Donner un résumé abstrait tout en gardant les importantes \
                        citations du discours en moins de {desired_length} mots: \n {content} \n",
        },
        "de": {
            "alias": "ml-summarization-german",
            "template": "Geben Sie eine abstrakte Zusammenfassung mit weniger als {desired_length} Wörtern und behalten \
                        Sie dabei wichtige Zitate: \n {content} \n",
        },
        "zh": {
            "alias": "ml-summarization-chinese",
            "template": "给出一个抽象的总结，同时保留重要的\
                        少于 {desired_length} 个单词的演讲引述：\n {content} \n",
        },
        "ko": {
            "alias": "ml-summarization-korean",
            "template": "다음 내용에 대해 중요한 인용구를 유지하면서 {desired_length} 단어 미만으로 요약하세요: \n {content} \n",
        },
        "fr": {
            "alias": "ml-summarization-korean",
            "template": "Donner un résumé abstrait tout en gardant l'importance \
                        citations de discours en moins de {desired_length} mots: \n {content} \n",
        },
        "fr": {
            "alias": "ml-summarization-korean",
            "template": "Donner un résumé abstrait tout en gardant l'importance \
                        citations de discours en moins de {desired_length} mots: \n {content} \n",
        },
    }


settings = Settings()
