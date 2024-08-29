# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""Helpers."""

# Standard Library
import os
from typing import Union

# 3rd party libraries
import pandas as pd

# Internal libraries
from onclusiveml.ts.constants import ROOT
from onclusiveml.ts.timeseries import TimeSeriesData


def load_data(file_name: str, reset_columns: bool = False) -> pd.DataFrame:
    """Load data for tests and tutorial notebooks."""
    root = os.path.join(os.getcwd(), ROOT)
    df = pd.read_csv(os.path.join(root, "data", file_name), encoding="utf8")
    if reset_columns:
        df.columns = ["time", "y"]
    return df


def load_air_passengers(return_ts: bool = True) -> Union[pd.DataFrame, TimeSeriesData]:
    """Load and return air passengers time series dataset.

    ==============================
    Length                     144
    Granularity              daily
    Label                     none

    Args:
        return_ts: return class:`onclusiveml.ts.timeseries.TimeSeriesData` by default
                   return `pandas.DataFrame` otherwise

    Returns:
        data: class:`onclusiveml.ts.timeseries.TimeSeriesData`
        file_name: `str`, the physical path of air passengers data set
        descr: `str`, full description of this data set

    Examples
    >>> from onclusiveml.ts.data import load_air_passengers
    >>> air_passengers_ts = load_air_passengers()
    >>> print(air_passengers_ts)
              time    y
        0   1949-01-01  112
        1   1949-02-01  118
        2   1949-03-01  132
        3   1949-04-01  129
        4   1949-05-01  121
        ..         ...  ...
        139 1960-08-01  606
        140 1960-09-01  508
        141 1960-10-01  461
        142 1960-11-01  390
        143 1960-12-01  432

        [144 rows x 2 columns]
    """
    df = load_data("air_passengers.csv")
    df.columns = ["time", "y"]

    if return_ts:
        return TimeSeriesData(df)
    else:
        return df
