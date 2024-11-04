"""Json Builder."""

# Standard Library
import json
import re


def build_json(text: str, keys: list) -> dict:
    """The main function for building the JSON.

    Args:
        text (str): The raw text containing JSON-like data or formatting.
        keys (list): A list of strings representing the keys to extract values for in the JSON structure.

    Returns:
        dict: A dictionary where each key from `keys` maps to a corresponding value extracted from `text`.
              If a key is not found, its value will be `None`. This method attempts to parse text as JSON
              directly if possible, otherwise it uses regular expressions and string processing to approximate
              the JSON structure.
    """
    json_raw = extract_json(text)
    # If we can't parse the text, the step below will
    # technically work; however there is a higherly
    # likelihood of having some of the formatting text
    # preserved in output
    if json_raw is None:
        json_raw = text

    try:
        return json.loads(json_raw)
    except json.JSONDecodeError:
        json_out = {}
        n_keys = len(keys)
        for i, key in enumerate(keys):
            # This is the main body of logic, we look
            # for text between the two keys using regular expressions
            start = find_start(json_raw, key)
            if i == n_keys - 1:
                end = len(text)
            else:
                end = find_end(json_raw, keys[i + 1])
            if start is None or end is None:
                json_out[key] = None
            else:
                string_raw = json_raw[start:end]
                value = clean_string(string_raw)
                json_out[key] = value
        return json_out


def extract_json(text: str) -> str:
    """This function uses regular expressions to parse the text file into a JSON.

    Args:
        text (str): The input text containing JSON-like data within specific delimiters.

    Returns:
        str: A string containing the raw JSON data if found within delimiters; otherwise, None.

    The extremely permissive structure of a JSON makes it difficult
    to be more specific in the capturing of body of the JSON.

    It is not a very sophisticated parsing, but
    closely mimics the functionality of LangChain's output
    parser, ie, anything surroned by ```json ```.

    This step isn't necessary.

    Subsequent steps can parse
    the output regardless; however, if this step is successfull
    it will remove junk punctuation from the final output.
    """
    try:
        pattern = "```json((?s).*)```"
        match = re.search(pattern, text)
        json_raw = match.group(1)
    except AttributeError:
        json_raw = None
    return json_raw


def find_start(text: str, key: str) -> str:
    """If the regex fails to find the key, then we return None.

    Args:
        text (str): The input text to search within.
        key (str): The key for which to find the start position in `text`.

    Returns:
        str: The end position of the key in `text` if found, otherwise None.

    Otherwise, we return the text end position of the pattern.
    """
    try:
        return re.search(f'"{key}": ', text).end()
    except AttributeError:
        return None


def find_end(text: str, key: str) -> str:
    """If the regex fails to find the next key, then we return None.

    Args:
        text (str): The input text to search within.
        key (str): The key for which to find the start of the following key's position.

    Returns:
        str: The start position of the next key in `text` if found, otherwise None.

    Otherwise, we return the text start position of the pattern.
    """
    try:
        return re.search(f'",\n\t"{key}": ', text).start()
    except AttributeError:
        try:
            # Trying a simplified version of the pattern
            return re.search(f'"{key}": ', text).start()
        except AttributeError:
            return None


def clean_string(string: str) -> str:
    """This is more of an example of what can be done than a firm recommendation.

    Args:
        string (str): The raw string extracted from the JSON-like data to clean.

    Returns:
        str: A cleaned version of the input string with extraneous punctuation and formatting removed.

    A great deal of punctuation and special characters that are used to structure
    the JSON can be removed to improve readability of the final product.
    """
    value = re.sub("[\n\t]", "", string)  # removing new lines and tabs
    value = re.sub('^"', "", value)  # removing starting quote
    # The order for removing junk at the end of a string
    # matters, first we want to remove the obvious problem,
    # which is the quote. That exposes a bunch of other problems
    value = re.sub('"$', "", value)  # removing trailing quote
    value = value.strip()  # removing leading and trailing white space
    value = re.sub('",$', "", value)  # removing unneeded end quote
    value = re.sub('"}$', "", value)  # removing unneeded brackets
    return value
