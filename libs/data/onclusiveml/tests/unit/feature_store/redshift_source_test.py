"""Custom redshift source test."""

# 3rd party libraries
import pytest
from feast.value_type import ValueType

# Internal libraries
from onclusiveml.data.feature_store.redshift_source import RedshiftSourceCustom


@pytest.fixture
def redshift_source_custom():
    """Creates an  Object of RedshiftSourceCustom class.

    Returns: Object of RedshiftSourceCustom class

    """
    return RedshiftSourceCustom(
        name="test_source",
        table="test_table",
        timestamp_field="timestamp",
        database="test-database",
        schema="public",
    )


def test_initialization(redshift_source_custom):
    """Test initialization of the object of RedshiftSourceCustom class.

    Args:
        redshift_source_custom: Object of RedshiftSourceCustom class

    Returns: None

    """
    assert redshift_source_custom.name == "test_source"
    assert redshift_source_custom.timestamp_field == "timestamp"
    assert redshift_source_custom.table == "test_table"
    assert redshift_source_custom.schema == "public"


def test_source_datatype_to_feast_value_type(redshift_source_custom):
    """Test if string redshift datatype is mapped to feast datatype.

    Args:
        redshift_source_custom:  Object of RedshiftSourceCustom class

    Returns: None

    """
    mapping_function = redshift_source_custom.source_datatype_to_feast_value_type()
    assert mapping_function("string") == ValueType.STRING
