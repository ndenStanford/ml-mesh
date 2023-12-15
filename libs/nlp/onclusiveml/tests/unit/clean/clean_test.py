"""Clean test."""

# Internal libraries
from onclusiveml.nlp.clean import clean


def test_remove_html_removes_tags():
    """Test remove_html function for removing HTML tags.

    Returns:
        None
    """
    input_text = "<p>This is <b>a sample</b> text.</p>"
    expected_output = "This is a sample text."
    res = clean.remove_html(input_text)
    assert res == expected_output


def test_remove_html_empty_text():
    """Test remove_html function for handling an empty string correctly.

    Returns:
        None
    """
    input_text = ""
    expected_output = ""
    res = clean.remove_html(input_text)
    assert res == expected_output


def test_remove_html_text_without_tags():
    """Test remove_html function for handling text without HTML tags correctly.

    Returns:
        None
    """
    input_text = "This is a sample text."
    expected_output = "This is a sample text."
    res = clean.remove_html(input_text)
    assert res == expected_output


def test_remove_whitespace():
    """Test remove_whitespace function for removing extra spaces.

    Returns:
        None
    """
    input_text = "This       is   a sample    text."
    expected_output = "This is a sample text."
    res = clean.remove_whitespace(input_text)
    assert res == expected_output


def test_remove_whitespace_empty_text():
    """Test remove_whitespace function for handling an empty string correctly.

    Returns:
        None
    """
    input_text = ""
    expected_output = ""
    res = clean.remove_whitespace(input_text)
    assert res == expected_output


def test_remove_whitespace_text_without_extra_spaces():
    """Test remove_whitespace function for handling text without extra spaces correctly.

    Returns:
        None
    """
    input_text = "This is a sample text."
    expected_output = "This is a sample text."
    res = clean.remove_whitespace(input_text)
    assert res == expected_output
