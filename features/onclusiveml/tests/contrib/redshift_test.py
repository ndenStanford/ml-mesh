"""Redshift test."""

from unittest import TestCase

from feast.value_type import ValueType
from parameterized.parameterized import parameterized
from onclusiveml.features.contrib.redshift import OnclusiveRedshiftSource


class OnclusiveRedshiftSourceValueTypeConversionTestCase(TestCase):
    """Test OnclusiveRedshiftSource `redshift_to_feast_value_type` method."""

    @parameterized.expand(
        [
            ("int2", ValueType.INT32),
            ("int4", ValueType.INT32),
            ("int8", ValueType.INT64),
            ("bigint", ValueType.INT64),
            ("numeric", ValueType.DOUBLE),
            ("float4", ValueType.FLOAT),
            ("float8", ValueType.DOUBLE),
            ("bool", ValueType.BOOL),
            ("character", ValueType.STRING),
            ("string", ValueType.STRING),
            ("varchar", ValueType.STRING),
            ("timestamp", ValueType.UNIX_TIMESTAMP),
            ("timestamptz", ValueType.UNIX_TIMESTAMP),
        ]
    )
    def test_redshift_to_feast_value_type(self, str_type: str, feast_value_type: ValueType) -> None:
        """Test spike."""
        assert OnclusiveRedshiftSource.redshift_to_feast_value_type(str_type) == feast_value_type
