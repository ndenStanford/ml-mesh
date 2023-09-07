"""Constants."""

# Internal libraries
from onclusiveml.core.base.utils import OnclusiveEnum


class PromptEnum(OnclusiveEnum):
    """Enum values for prompts."""

    EN = [
        "Give an abstractive summary while retaining important quotes of speech in less than "
        + "{number}"  # noqa: W503
        + " words: "  # noqa: W503
        + "\n"  # noqa: W503
        + "{text}"  # noqa: W503
        + "\n",  # noqa: W503
        "english-summarization",
        {"model_name": "gpt-3.5-turbo", "max_tokens": 512, "temperature": 0.7},
    ]
    ML_SEG = [
        "Do a segmentation unifying the main stories of this text in their given language and "
        + "output a json object where the key is the start time code and "  # noqa: W503
        + "the value is the headline of the main stories: {transcript}",  # noqa: W503
        "ml-transcript-segmentation",
        {"model_name": "gpt-4", "max_tokens": 2048, "temperature": 0},
    ]
