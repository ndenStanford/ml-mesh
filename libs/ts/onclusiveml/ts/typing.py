"""Typing."""

# Standard Library
from datetime import datetime, timedelta
from typing import Sequence, Tuple, Union

# 3rd party libraries
import numpy as np
import pandas as pd


Figsize = Tuple[int, int]
# A TimedeltaLike object represents a time offset.
# E.g., length of 1 day can be represented by timedelta(days=1),or by
# a timestamp offset 86400, or by the offset alias "1D" defined in pandas
TimedeltaLike = Union[timedelta, float, str]


Timestamp = Union[str, pd.Timestamp, datetime]
ArrayLike = Union[np.ndarray, Sequence[float]]
