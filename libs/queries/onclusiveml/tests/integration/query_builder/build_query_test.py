"""Build query Test."""

# 3rd party libraries
import pytest  # noqa


def test_query_builder(test_query_builder, expected_query_builder):
    """Test query builder."""
    expected_test_el = expected_query_builder["test_el"]
    expected_test_ner = expected_query_builder["test_ner"]
    expected_test_regex = expected_query_builder["test_regex"]

    actual_test_el, actual_test_ner, actual_test_regex = test_query_builder

    assert actual_test_el == expected_test_el
    assert actual_test_ner == expected_test_ner
    assert actual_test_regex == expected_test_regex
