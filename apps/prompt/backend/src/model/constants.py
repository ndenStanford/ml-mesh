"""Constants"""

# Standard Library
from enum import Enum


class ModelEnum(Enum):
    """Enum values for models"""

    GPT3_5 = "gpt-3.5-turbo"
    GPT4 = "gpt-4"
    DAVINCI = "text-davinci-003"
    CURIE = "text-curie-001"
