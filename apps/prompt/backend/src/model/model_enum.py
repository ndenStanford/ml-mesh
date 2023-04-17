"""Model Enum"""

# Standard Library
from enum import Enum


class ModelEnum(Enum):
    GPT3_5 = "gpt-3.5-turbo"
    GPT4 = "gpt-4"
    DAVINCI = "text-davinci-003"
    CURIE = "text-curie-001"
