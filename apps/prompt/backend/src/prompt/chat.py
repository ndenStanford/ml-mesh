""" Constants """

# 3rd party libraries
from pydantic import BaseModel


class PromptChat(BaseModel):
    """
    Class to represent values that come from prompt chat ui

    Args:
        prompt (str): prompt input from chat

    """

    prompt: str
