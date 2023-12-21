"""Preprocess test."""

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.nlp import preprocess


@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        ("<p>This is <b>a sample</b> text.</p>", "This is a sample text."),
        ("", ""),
        ("This is a sample text.", "This is a sample text."),
    ],
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
    "input_text, input_regex, expected_output",
    [
        ("This    is   a   sample   text.", r"\s+", "This is a sample text."),
        ("", r"\s+", ""),
        ("This is a sample text.", r"\s+", "This is a sample text."),
        ("    This   is   a  sample  text.", r"\s+", " This is a sample text."),
        ("This___is___a___sample___text.", r"_+", "This is a sample text."),
    ],
)
def test_remove_whitespace(input_text, input_regex, expected_output):
    """Test remove_whitespace function with various inputs and regex.

    Args:
        input_text (str): Text with extra spaces
        expected_output (str): Expected output after removing extra spaces

    Returns:
        None
    """
    res = preprocess.remove_whitespace(input_text, input_regex)
    assert res == expected_output
