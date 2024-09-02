# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""Exceptions."""


class TimeSeriesException(Exception):
    """Time Series Exception."""


class DataException(TimeSeriesException):
    """Data Exception."""


class IrregularGranularityException(DataException):
    """Irregular granularity exception."""


class InsufficientDataException(DataException):
    """Insufficient data exeption."""


class ParameterError(TimeSeriesException):
    """Parameter error."""


class InternalError(TimeSeriesException):
    """Internal error."""
