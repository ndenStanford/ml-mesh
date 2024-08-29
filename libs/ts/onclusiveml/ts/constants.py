# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""Constants."""


# Standard Library
from enum import Enum, IntEnum, auto, unique


# Constants
ROOT = "libs/ts/onclusiveml/ts"
DEFAULT_TIME_NAME = "time"  # Default name for the time column in TimeSeriesData
DEFAULT_VALUE_NAME = "value"  # Default name for the value column in TimeSeriesData
# Internal prefix used when merging two TimeSeriesData objects
PREFIX_OP_1 = "_onclusiveml.ts.1"
# Second internal prefix used when merging two TimeSeriesData objects
PREFIX_OP_2 = "_onclusiveml.ts.2"
INTERPOLATION_METHODS = {
    "linear",
    "bfill",
    "ffill",
}  # List of possible interpolation methods

IRREGULAR_GRANULARITY_ERROR = (
    "This algorithm or this parameter setup does not support input data with irregular data granularity. "
    "Please update your query to ensure that your data have fixed granularity."
)


class MetricType(Enum):
    """Metrics can be scores, errors, or neither."""

    NONE = 0
    """Neither score nor error"""

    SCORE = 1
    """Larger is better (1 is better than 0)"""

    ERROR = 2
    """Closer to zero is better (0 is better than 1 or -1)"""


class Directionality(IntEnum):
    """Metrics can improve in a direction (up or down) or lack clear direction.

    Non-negative error metrics are negative and vice-versa because lower values
    are also closer to zero. However, metrics that can result in negative values
    cannot be simultaneously NEGATIVE and ERROR.
    """

    NONE = 0
    """Neither positive nor negative."""

    POSITIVE = 1
    """Larger is better  (1 is better than 0)"""

    NEGATIVE = -1
    """Smaller is better (-1 better than 0 better than 1)"""


@unique
class OperationsEnum(Enum):
    """Mathematical operations that can be performed on:class:`TimeSeriesData` objects."""

    ADD = auto()
    SUB = auto()
    DIV = auto()
    MUL = auto()
