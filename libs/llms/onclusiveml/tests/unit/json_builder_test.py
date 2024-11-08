"""Test JSON builder."""

# Internal libraries
from onclusiveml.llms.json_builder import (
    build_json,
    clean_string,
    extract_json,
    find_end,
    find_start,
)


def test_valid_json_block():
    """Test extracting a valid JSON block from text."""
    text = 'Some text before ```json{"key": "value"}``` some text after'
    expected = '{"key": "value"}'
    assert extract_json(text) == expected


def test_valid_json_block_multiline():
    """Test extracting a multiline JSON block from text."""
    text = """Some text before ```json
    {
        "key": "value",
        "number": 123
    }
    ``` some text after"""
    expected = """
    {
        "key": "value",
        "number": 123
    }
    """
    assert extract_json(text) == expected


def test_no_json_block():
    """Test handling text without a JSON block."""
    text = "Some text without json block"
    assert extract_json(text) is None


def test_empty_string_extract_json():
    """Test handling an empty string input for extract_json."""
    text = ""
    assert extract_json(text) is None


def test_json_block_with_additional_markdown():
    """Test extracting a JSON block with additional markdown in text."""
    text = 'Some text ```json{"key": "value"}``` **bold text**'
    expected = '{"key": "value"}'
    assert extract_json(text) == expected


def test_key_present():
    """Test finding the start position of a key in text."""
    text = '"key": "value"'
    key = "key"
    expected = text.find(f'"{key}": ') + len(f'"{key}": ')
    assert find_start(text, key) == expected


def test_key_absent():
    """Test handling when a key is absent in text."""
    text = '"another_key": "value"'
    key = "key"
    assert find_start(text, key) is None


def test_empty_text_find_start():
    """Test find_start with empty text."""
    text = ""
    key = "key"
    assert find_start(text, key) is None


def test_empty_key_find_start():
    """Test find_start with an empty key."""
    text = '"key": "value"'
    key = ""
    assert find_start(text, key) is None


def test_special_characters_in_key():
    """Test find_start with a key containing special characters."""
    text = '"k£y!@": "value"'
    key = "k£y!@"
    expected = text.find(f'"{key}": ') + len(f'"{key}": ')
    assert find_start(text, key) == expected


def test_next_key_present():
    """Test finding the end position before the next key in text."""
    text = '"key": "value",\n\t"next_key": "next_value"'
    key = "next_key"
    expected = text.find(f'",\n\t"{key}": ')
    assert find_end(text, key) == expected


def test_next_key_absent():
    """Test handling when the next key is absent in text."""
    text = '"key": "value"'
    key = "next_key"
    assert find_end(text, key) is None


def test_simplified_pattern():
    """Test find_end with a simplified pattern when the standard pattern fails."""
    text = '"key": "value", "next_key": "next_value"'
    key = "next_key"
    expected = text.find(f'"{key}": ')
    assert find_end(text, key) == expected


def test_empty_text_find_end():
    """Test find_end with empty text."""
    text = ""
    key = "next_key"
    assert find_end(text, key) is None


def test_empty_key_find_end():
    """Test find_end with an empty key."""
    text = '"key": "value"'
    key = ""
    assert find_end(text, key) is None


def test_standard_string():
    """Test cleaning a standard string with newlines and tabs."""
    string = '\n\t"value"\n\t'
    expected = "value"
    assert clean_string(string) == expected


def test_string_with_quotes():
    """Test cleaning a string that includes quotes."""
    string = '"value"'
    expected = "value"
    assert clean_string(string) == expected


def test_string_with_extra_commas():
    """Test cleaning a string with extra commas at the end."""
    string = '"value",'
    expected = "value"
    assert clean_string(string) == expected


def test_string_with_brackets():
    """Test cleaning a string that ends with a bracket."""
    string = '"value"}'
    expected = "value"
    assert clean_string(string) == expected


def test_empty_string_clean_string():
    """Test cleaning an empty string."""
    string = ""
    expected = ""
    assert clean_string(string) == expected


def test_string_with_whitespace():
    """Test cleaning a string with leading and trailing whitespace."""
    string = '    "value"    '
    expected = '"value"'
    assert clean_string(string) == expected


def test_complex_string():
    """Test cleaning a complex string with commas and brackets."""
    string = '\n\t"complex, value"}\n\t'
    expected = "complex, value"
    assert clean_string(string) == expected


def test_valid_json_input():
    """Test building JSON from valid JSON input."""
    text = '{"key": "value", "number": 123}'
    keys = ["key", "number"]
    expected = {"key": "value", "number": 123}
    assert build_json(text, keys) == expected


def test_invalid_json_fallback():
    """Test building JSON when input is invalid and fallback parsing is used."""
    text = 'Some invalid text "key": "value", "number": 123'
    keys = ["key", "number"]
    expected = {"key": "value", "number": "123"}
    assert build_json(text, keys) == expected


def test_missing_keys():
    """Test handling missing keys when building JSON."""
    text = '{"key": "value"}'
    keys = ["key", "number"]
    expected = {"key": "value", "number": None}
    assert build_json(text, keys) == expected


def test_empty_text_build_json():
    """Test building JSON from empty text input."""
    text = ""
    keys = ["key"]
    expected = {"key": None}
    assert build_json(text, keys) == expected


def test_text_with_json_block():
    """Test building JSON from text that includes a JSON block."""
    text = 'Some text ```json{"key": "value", "number": 123}``` more text'
    keys = ["key", "number"]
    expected = {"key": "value", "number": 123}
    assert build_json(text, keys) == expected


def test_keys_not_in_order():
    """Test building JSON when keys are not in order."""
    text = '{"number": 123, "key": "value"}'
    keys = ["key", "number"]
    expected = {"key": "value", "number": 123}
    assert build_json(text, keys) == expected


def test_complex_text_with_formatting():
    """Test building JSON from complex text with formatting."""
    text = """
    Here is some text
    ```json
    {
        "key": "value",
        "details": {
            "number": 123,
            "status": "active"
        }
    }
    ```
    And some more text
    """
    keys = ["key", "details"]
    expected = {"key": "value", "details": {"number": 123, "status": "active"}}
    assert build_json(text, keys) == expected


def test_non_json_text():
    """Test building JSON from text without any JSON data."""
    text = "Just some random text without JSON"
    keys = ["key"]
    expected = {"key": None}
    assert build_json(text, keys) == expected


def test_partial_json_in_text():
    """Test building JSON from text that contains partial JSON."""
    text = 'Some text {"key": "value"}'
    keys = ["key"]
    expected = {"key": "value"}
    assert build_json(text, keys) == expected


def test_key_with_special_characters():
    """Test building JSON when keys have special characters."""
    text = '{"k$e@y!": "value"}'
    keys = ["k$e@y!"]
    expected = {"k$e@y!": "value"}
    assert build_json(text, keys) == expected


def test_numeric_values():
    """Test building JSON with numeric values."""
    text = '{"number": 123, "float": 456.78}'
    keys = ["number", "float"]
    expected = {"number": 123, "float": 456.78}
    assert build_json(text, keys) == expected


def test_boolean_and_null_values():
    """Test building JSON with boolean and null values."""
    text = '{"active": true, "value": null}'
    keys = ["active", "value"]
    expected = {"active": True, "value": None}
    assert build_json(text, keys) == expected


def test_list_values():
    """Test building JSON with list values."""
    text = '{"items": [1, 2, 3]}'
    keys = ["items"]
    expected = {"items": [1, 2, 3]}
    assert build_json(text, keys) == expected


def test_nested_json_objects():
    """Test building JSON with nested JSON objects."""
    text = '{"user": {"name": "Alice", "age": 30}}'
    keys = ["user"]
    expected = {"user": {"name": "Alice", "age": 30}}
    assert build_json(text, keys) == expected


def test_exception_handling_invalid_json():
    """Test building JSON when input JSON is invalid."""
    text = '{"key": "value", "number": }'  # Invalid JSON
    keys = ["key", "number"]
    expected = {"key": "value", "number": None}
    assert build_json(text, keys) == expected


def test_large_input_text():
    """Test building JSON with a large input text."""
    text = '{"key": "' + "a" * 1000 + '"}'
    keys = ["key"]
    expected = {"key": "a" * 1000}
    assert build_json(text, keys) == expected


def test_unicode_characters():
    """Test building JSON with unicode characters."""
    text = '{"key": "välüe", "emoji": ":blush:"}'
    keys = ["key", "emoji"]
    expected = {"key": "välüe", "emoji": ":blush:"}
    assert build_json(text, keys) == expected


def test_input_with_tabs_and_newlines():
    """Test building JSON from input with tabs and newlines."""
    text = '\n\t{\n\t"key":\n\t"value"\n\t}\n\t'
    keys = ["key"]
    expected = {"key": "value"}
    assert build_json(text, keys) == expected
