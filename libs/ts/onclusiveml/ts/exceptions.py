# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


class TimeSeriesError(Exception):
    pass


class DataError(TimeSeriesError):
    pass


class DataIrregularGranularityError(DataError):
    pass


class DataInsufficientError(DataError):
    pass


class ParameterError(TimeSeriesError):
    pass


class InternalError(TimeSeriesError):
    pass
