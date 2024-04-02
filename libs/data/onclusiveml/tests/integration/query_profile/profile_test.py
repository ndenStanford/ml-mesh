"""profile test."""

# 3rd party libraries
import pytest  # noqa

# Internal libraries
from onclusiveml.data.query_profile import MediaAPISettings, StringQueryProfile


def test_profile(input_query, expected_output):
    """Test query profile."""
    settings = MediaAPISettings()
    query = StringQueryProfile(string_query=input_query)
    es_query = query.es_query(settings)
    assert es_query == expected_output
