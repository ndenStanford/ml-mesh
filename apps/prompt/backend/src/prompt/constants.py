"""Constants"""

# Standard Library
from enum import Enum


class PromptEnum(Enum):
    """Enum values for models"""

    EN = [
        "Give an abstractive summary while retaining important quotes of speech in less than "
        + "{number}"  # noqa: W503
        + " words: "  # noqa: W503
        + "\n"  # noqa: W503
        + "{text}"  # noqa: W503
        + "\n",  # noqa: W503
        "English Summarization",
    ]
