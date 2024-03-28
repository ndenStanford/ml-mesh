"""profile test."""

# 3rd party libraries
import pytest  # noqa

# Internal libraries
from onclusiveml.data.query_profile import MediaAPISettings, StringQueryProfile


def test_profile(get_secret, input_query, expected_output):
    """Test query profile."""
    client_id, client_secret = get_secret
    settings = MediaAPISettings(client_id=client_id, client_secret=client_secret)
    query = StringQueryProfile(string_query=input_query)
    es_query = query.es_query(settings)
    assert es_query == expected_output
