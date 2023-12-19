"""Preprocess."""

# Standard Library
import re

# 3rd party libraries
from bs4 import BeautifulSoup


def remove_html(text: str) -> str:
    """Remove HTML tags from input text.

    Args:
        text (str): Input text

    Returns:
        str: Text with HTML tags removed
    """
    text = BeautifulSoup(text, "html.parser").text

    return text


def remove_whitespace(text: str, regex: str = r"\s+") -> str:
    r"""Remove extra white spaces from input text.

    Args:
        text (str): Input text
        regex (str, optional): Regex pattern for whitespace removal. Defaults to r"\\s+".

    Returns:
        str: Text with extra whitespaces removed
    """
    text = re.sub(regex, " ", text)

    return text
