"""Preprocess test."""

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.nlp import preprocess


list_of_inputs_with_expected_output_for_html_removal = [
    ("<p>This is <b>a sample</b> text.</p>", "This is a sample text."),
    ("", ""),
    ("This is a sample text.", "This is a sample text."),
]

list_of_inputs_with_expected_output_for_whitspace_removal = [
    ("This    is   a   sample   text.", "This is a sample text."),
    ("", ""),
    ("This is a sample text.", "This is a sample text."),
    (" This   is   a  sample  text.", " This is a sample text."),
]


@pytest.mark.parametrize(
    "input_text, expected_output", list_of_inputs_with_expected_output_for_html_removal
)
def test_remove_html(input_text, expected_output):
    """Test remove_html function with various inputs.

    Args:
        input_text (str): input text
        expected_output (str): Expected output after HTML tag removal

    Returns:
        None
    """
    res = preprocess.remove_html(input_text)
    assert res == expected_output


@pytest.mark.parametrize(
    "input_text, expected_output",
    list_of_inputs_with_expected_output_for_whitspace_removal,
)
def test_remove_whitespace(input_text, expected_output):
    """Test remove_whitespace function with various inputs.

    Args:
        input_text (str): Text with extra spaces
        expected_output (str): Expected output after removing extra spaces

    Returns:
        None
    """
    res = preprocess.remove_whitespace(input_text)
    assert res == expected_output


def test_remove_whitespace_custom_regex():
    """Test remove_whitespace function with a user-provided regex.

    Returns:
        None
    """
    input_text = "This___is___a___sample___text."
    expected_output = "This is a sample text."
    custom_regex = r"_+"
    res = preprocess.remove_whitespace(input_text, regex=custom_regex)
    assert res == expected_output
