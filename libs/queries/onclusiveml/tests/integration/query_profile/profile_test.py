"""profile test."""

# 3rd party libraries
import pytest  # noqa

# Internal libraries
from onclusiveml.queries.query_profile import (
    MediaAPISettings,
    MediaApiStringQuery,
    ProductionToolsQueryProfile,
    StringQueryProfile,
)


def test_profile(input_query, expected_output):
    """Test query profile."""
    settings = MediaAPISettings()
    query = StringQueryProfile(string_query=input_query)
    es_query = query.es_query(settings)
    assert es_query == expected_output


def test_production_tool(
    input_query_id,
    input_product_tool_version,
    expected_query_id_output,
    expected_output,
):
    """Test production tool."""
    settings = MediaAPISettings()
    boolean_id = ProductionToolsQueryProfile(
        version=input_product_tool_version, query_id=input_query_id
    )
    str_query = boolean_id.query
    assert str_query == expected_query_id_output
    es_query = boolean_id.es_query(settings)
    assert es_query == expected_output


def test_media_api_query(input_media_api_query, expected_media_query):
    """Test media api query."""
    settings = MediaAPISettings()
    query = MediaApiStringQuery(string_query=input_media_api_query)
    es_query = query.es_query(settings)
    assert es_query == expected_media_query
