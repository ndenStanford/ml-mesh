"""Timestamp Offsets."""

# Internal libraries
from onclusiveml.core.base import OnclusiveEnum


class OffsetEnum(OnclusiveEnum):
    """Offset Enums in miliseconds.

    Please see https://app.neptune.ai/o/onclusive/org/large-language-models/n/9bca0480-0a48-4ad5-a8f4-378ec945fc24/9bd66593-37bf-4912-9a45-74e44612fb61. # noqa: E501, W505
    """

    GBR = {"start_offset": -7933, "end_offset": -7933}
    ESP = {"start_offset": -266, "end_offset": 734}
    FRA = {"start_offset": -266, "end_offset": -266}
