"""Custom Redshift source for feast feature store."""

# Standard Library
from typing import Callable, Dict, Optional

# 3rd party libraries
from feature_store_handle import RedshiftSource, type_map
from feature_store_handle.value_type import ValueType


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
    def source_datatype_to_feast_value_type() -> Callable[[str], ValueType]:
        """Returns: Callable[[str], ValueType] : A map of redshift to feast value types."""
        redshift_to_feast_value_type_custom = type_map.redshift_to_feast_value_type
        redshift_to_feast_value_type_custom["string"] = ValueType.STRING
        return redshift_to_feast_value_type_custom
