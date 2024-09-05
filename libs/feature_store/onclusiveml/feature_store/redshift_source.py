"""Custom Redshift source for feast feature store."""

# Standard Library
from typing import Callable, Dict, Optional

# 3rd party libraries
from feast import RedshiftSource
from feast.value_type import ValueType


class RedshiftSourceCustom(RedshiftSource):
    """Custom Redshift source for feast feature store."""

    def __init__(
        self,
        *,
        name: Optional[str] = None,
        timestamp_field: Optional[str] = "",
        table: Optional[str] = None,
        schema: Optional[str] = None,
        created_timestamp_column: Optional[str] = "",
        field_mapping: Optional[Dict[str, str]] = None,
        query: Optional[str] = None,
        description: Optional[str] = "",
        tags: Optional[Dict[str, str]] = None,
        owner: Optional[str] = "",
        database: Optional[str] = "",
    ):
        super().__init__(
            name=name,
            timestamp_field=timestamp_field,
            table=table,
            schema=schema,
            created_timestamp_column=created_timestamp_column,
            field_mapping=field_mapping,
            query=query,
            description=description,
            tags=tags,
            owner=owner,
            database=database,
        )

    @staticmethod
    def redshift_to_feast_value_type(redshift_type_as_str: str) -> ValueType:
        """Type names from https://docs.aws.amazon.com/redshift/latest/dg/c_Supported_data_types.html.

        Args:
            redshift_type_as_str: Input redshift type to be mapped to feast datatype

        Returns: Feast datatype to be mapped to redshift datatype

        """
        type_map = {
            "int2": ValueType.INT32,
            "int4": ValueType.INT32,
            "int8": ValueType.INT64,
            "bigint": ValueType.INT64,
            "numeric": ValueType.DOUBLE,
            "float4": ValueType.FLOAT,
            "float8": ValueType.DOUBLE,
            "bool": ValueType.BOOL,
            "character": ValueType.STRING,
            "string": ValueType.STRING,
            "varchar": ValueType.STRING,
            "timestamp": ValueType.UNIX_TIMESTAMP,
            "timestamptz": ValueType.UNIX_TIMESTAMP,
            # skip date, geometry, hllsketch, time, timetz
        }

        return type_map[redshift_type_as_str.lower()]

    def source_datatype_to_feast_value_type(self) -> Callable[[str], ValueType]:
        """Returns: Callable[[str], ValueType] : A map of redshift to feast value types."""
        return self.redshift_to_feast_value_type
