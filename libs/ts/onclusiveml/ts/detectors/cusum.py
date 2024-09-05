# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""CUSUMDetectorModel is a wraper of CUSUMDetector to detect multiple change points.

Typical usage example:

>>> # Define CUSUMDetectorModel
>>> model = CUSUMDetectorModel(
        scan_window=43200,
        historical_window=604800,
        threshold=0.01,
        delta_std_ratio=1.0,
        serialized_model=None,
        change_directions=["increase"],
        score_func=CusumScoreFunction.percentage_change,
        remove_seasonality=True,
    )
>>> # Run detector
>>> respond = model.fit_predict(tsd)
>>> # Plot anomaly score
>>> respond.scores.plot(cols=['value'])
>>> # Get change points in unixtime
>>> change_points = model.cps
"""

# Standard Library
import json
import logging
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from typing import (
    Any,
    Dict,
    List,
    NamedTuple,
    Optional,
    Sequence,
    Tuple,
    Union,
    cast,
)

# 3rd party libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import chi2

# Internal libraries
from onclusiveml.ts.base.detector import Detector, DetectorModel
from onclusiveml.ts.constants import (
    DEFAULT_VALUE_NAME,
    IRREGULAR_GRANULARITY_ERROR,
)
from onclusiveml.ts.decomposition import SeasonalityHandler
from onclusiveml.ts.detectors.constants import AnomalyResponse
from onclusiveml.ts.exceptions import (
    InternalError,
    IrregularGranularityException,
    ParameterError,
)
from onclusiveml.ts.timeseries import TimeSeriesChangePoint, TimeSeriesData


pd.options.plotting.matplotlib.register_converters = True

NORMAL_TOLERENCE = 1  # number of window
CHANGEPOINT_RETENTION: int = 7 * 24 * 60 * 60  # in seconds
MAX_CHANGEPOINT = 10

_log: logging.Logger = logging.getLogger("cusum_model")


@dataclass
class CUSUMDefaultArgs:
    """Cusum Default arguments."""

    threshold: float = 0.01
    max_iter: int = 10
    delta_std_ratio: float = 1.0
    min_abs_change: int = 0
    start_point: Optional[int] = None
    change_directions: Optional[List[str]] = None
    interest_window: Optional[int] = None
    magnitude_quantile: Optional[float] = None
    magnitude_ratio: float = 1.3
    magnitude_comparable_day: float = 0.5
    return_all_changepoints: bool = False
    remove_seasonality: bool = False


@dataclass
class CUSUMChangePointVal:
    """Cusum change point value."""

    changepoint: int
    mu0: float
    mu1: float
    changetime: float
    stable_changepoint: bool
    delta: float
    llr_int: float
    p_value_int: float
    delta_int: Optional[float]
    sigma0: Optional[float] = None
    sigma1: Optional[float] = None
    llr: Optional[float] = None
    p_value: Optional[float] = None
    regression_detected: Optional[bool] = None


@dataclass
class VectorizedCUSUMChangePointVal:
    """Vectorized cusum change point value."""

    changepoint: List[int]
    mu0: List[float]
    mu1: List[float]
    changetime: List[float]
    stable_changepoint: List[bool]
    delta: List[float]
    llr_int: List[float]
    p_value_int: List[float]
    delta_int: Optional[List[float]]
    sigma0: Optional[List[float]] = None
    sigma1: Optional[List[float]] = None
    llr: Optional[List[float]] = None
    p_value: Optional[List[float]] = None
    regression_detected: Optional[List[bool]] = None


def transfer_vect_cusum_cp_to_cusum_cp(
    vectcusumcp: VectorizedCUSUMChangePointVal,
) -> List[CUSUMChangePointVal]:
    """Transfer vector cusum changepoint to cusum changepoint."""
    res = []
    for i in range(len(vectcusumcp.changepoint)):
        res.append(
            CUSUMChangePointVal(
                changepoint=vectcusumcp.changepoint[i],
                mu0=vectcusumcp.mu0[i],
                mu1=vectcusumcp.mu1[i],
                changetime=vectcusumcp.changetime[i],
                stable_changepoint=vectcusumcp.stable_changepoint[i],
                delta=vectcusumcp.delta[i],
                llr_int=vectcusumcp.llr_int[i],
                p_value_int=vectcusumcp.p_value_int[i],
                delta_int=vectcusumcp.delta_int[i],
            )
        )
    return res


class CUSUMChangePoint(TimeSeriesChangePoint):
    """CUSUM change point.

    This is a changepoint detected by CUSUMDetector.

    Attributes:
        start_time: Start time of the change.
        end_time: End time of the change.
        confidence: The confidence of the change point.
        direction: a str stand for the changepoint change direction 'increase'
            or 'decrease'.
        cp_index: an int for changepoint index.
        mu0: a float indicates the mean before changepoint.
        mu1: a float indicates the mean after changepoint.
        delta: mu1 - mu0.
        llr: log likelihood ratio.
        llr_int: log likelihood ratio in the interest window.
        regression_detected: a bool indicates if regression detected.
        stable_changepoint: a bool indicates if we have a stable changepoint
            when locating the changepoint.
        p_value: p_value of the changepoint.
        p_value_int: p_value of the changepoint in the interest window.
    """

    def __init__(
        self,
        # pyre-fixme[11]: Annotation `Timestamp` is not defined as a type.
        start_time: pd.Timestamp,
        end_time: pd.Timestamp,
        confidence: float,
        direction: str,
        cp_index: int,
        mu0: Union[float, np.ndarray],
        mu1: Union[float, np.ndarray],
        delta: Union[float, np.ndarray],
        llr_int: float,
        llr: float,
        regression_detected: bool,
        stable_changepoint: bool,
        p_value: float,
        p_value_int: float,
    ) -> None:
        super().__init__(start_time, end_time, confidence)
        self._direction = direction
        self._cp_index = cp_index
        self._mu0 = mu0
        self._mu1 = mu1
        self._delta = delta
        self._llr_int = llr_int
        self._llr = llr
        self._regression_detected = regression_detected
        self._stable_changepoint = stable_changepoint
        self._p_value = p_value
        self._p_value_int = p_value_int

    @property
    def direction(self) -> str:
        """Direction."""
        return self._direction

    @property
    def cp_index(self) -> int:
        """Changepoint index."""
        return self._cp_index

    @property
    def mu0(self) -> Union[float, np.ndarray]:
        """Parameter mu0."""
        return self._mu0

    @property
    def mu1(self) -> Union[float, np.ndarray]:
        """Parameter mu1."""
        return self._mu1

    @property
    def delta(self) -> Union[float, np.ndarray]:
        """Parameter delta."""
        return self._delta

    @property
    def llr(self) -> float:
        """Parameter llr."""
        return self._llr

    @property
    def llr_int(self) -> float:
        """Parameter llr int."""
        return self._llr_int

    @property
    def regression_detected(self) -> bool:
        """Regression detected."""
        return self._regression_detected

    @property
    def stable_changepoint(self) -> bool:
        """Stable changepoint."""
        return self._stable_changepoint

    @property
    def p_value(self) -> float:
        """P-value."""
        return self._p_value

    @property
    def p_value_int(self) -> float:
        """P-value int."""
        return self._p_value_int

    def __repr__(self) -> str:
        return (
            f"CUSUMChangePoint(start_time: {self._start_time}, end_time: "
            f"{self._end_time}, confidence: {self._confidence}, direction: "
            f"{self._direction}, index: {self._cp_index}, delta: {self._delta}, "
            f"regression_detected: {self._regression_detected}, "
            f"stable_changepoint: {self._stable_changepoint}, mu0: {self._mu0}, "
            f"mu1: {self._mu1}, llr: {self._llr}, llr_int: {self._llr_int}, "
            f"p_value: {self._p_value}, p_value_int: {self._p_value_int})"
        )

    def __eq__(self, other: TimeSeriesChangePoint) -> bool:
        if not isinstance(other, CUSUMChangePoint):
            # don't attempt to compare against unrelated types
            raise NotImplementedError

        return (
            self._start_time == other._start_time
            and self._end_time == other._end_time
            and self._confidence == other._confidence
            and self._direction == other._direction
            and self._cp_index == other._cp_index
            and self._delta == other._delta
            and self._regression_detected == other._regression_detected
            and self._stable_changepoint == other._stable_changepoint
            and self._mu0 == other._mu0
            and self._mu1 == other._mu1
            and self._llr == other._llr
            and self._llr_int == other._llr_int
            and self._p_value == other._p_value
            # and self._p_value_int == other._p_value_int
        )

    def _almost_equal(self, x: float, y: float, round_int: int = 10) -> bool:
        """Almost equal."""
        return (
            x == y
            or round(x, round_int) == round(y, round_int)
            or round(abs((y - x) / x), round_int) == 0
        )

    def almost_equal(self, other: TimeSeriesChangePoint, round_int: int = 10) -> bool:
        """Compare if two CUSUMChangePoint objects are almost equal to each other."""
        if not isinstance(other, CUSUMChangePoint):
            # don't attempt to compare against unrelated types
            raise NotImplementedError

        res = [
            self._start_time == other._start_time,
            self._end_time == other._end_time,
            self._almost_equal(self._confidence, other._confidence, round_int),
            self._direction == other._direction,
            self._cp_index == other._cp_index,
            self._almost_equal(self._delta, other._delta, round_int),
            self._regression_detected == other._regression_detected,
            self._stable_changepoint == other._stable_changepoint,
            self._almost_equal(self._mu0, other._mu0, round_int),
            self._almost_equal(self._mu1, other._mu1, round_int),
            self._almost_equal(self._llr, other._llr, round_int),
            self._almost_equal(self._llr_int, other._llr_int, round_int),
            self._almost_equal(self._p_value, other._p_value, round_int),
        ]

        return all(res)


class CUSUMDetector(Detector):
    """Cusum detector."""

    interest_window: Optional[Tuple[int, int]] = None
    magnitude_quantile: Optional[float] = None
    magnitude_ratio: Optional[float] = None
    changes_meta: Optional[Dict[str, Dict[str, Any]]] = None

    def __init__(
        self,
        data: TimeSeriesData,
        is_multivariate: bool = False,
        is_vectorized: bool = False,
    ) -> None:
        """Univariate CUSUM detector for level shifts.

        Use cusum to detect changes, the algorithm is based on likelihood ratio
        cusum. See https://www.fs.isy.liu.se/Edu/Courses/TSFS06/PDFs/Basseville.pdf
        for details. This detector is used to detect mean changes in Normal
        Distribution.

        Args:
            data (TimeSeriesData): The input time series data.
            is_multivariate (bool): should be False unless running
                MultiCUSUMDetector
            is_vectorized (bool): should be False unless running
                VectorizedCUSUMDetector
        """
        super(CUSUMDetector, self).__init__(data=data)
        if not self.data.is_univariate() and not is_multivariate and not is_vectorized:
            msg = (
                "CUSUMDetector only supports univariate time series, but got "
                f"{type(self.data.value)}.  For multivariate time series, use "
                "MultiCUSUMDetector or VectorizedCUSUMDetector"
            )
            _log.error(msg)
            raise ValueError(msg)

    def _get_change_point(
        self, ts: np.ndarray, max_iter: int, start_point: int, change_direction: str
    ) -> CUSUMChangePointVal:
        """Find change point in the timeseries."""
        interest_window = self.interest_window
        # locate the change point using cusum method
        if change_direction == "increase":
            changepoint_func = np.argmin
            _log.debug("Detecting increase changepoint.")
        else:
            assert change_direction == "decrease"
            changepoint_func = np.argmax
            _log.debug("Detecting decrease changepoint.")
        n = 0
        # use the middle point as initial change point to estimate mu0 and mu1
        if interest_window is not None:
            ts_int = ts[interest_window[0] : interest_window[1]]
        else:
            ts_int = ts

        if start_point is None:
            cusum_ts = np.cumsum(ts_int - np.mean(ts_int))
            changepoint = min(changepoint_func(cusum_ts), len(ts_int) - 2)
        else:
            changepoint = start_point

        mu0 = mu1 = None
        # iterate until the changepoint converage
        while n < max_iter:
            n += 1
            mu0 = np.mean(ts_int[: (changepoint + 1)])
            mu1 = np.mean(ts_int[(changepoint + 1) :])
            mean = (mu0 + mu1) / 2
            # here is where cusum is happening
            cusum_ts = np.cumsum(ts_int - mean)
            next_changepoint = max(1, min(changepoint_func(cusum_ts), len(ts_int) - 2))
            if next_changepoint == changepoint:
                break
            changepoint = next_changepoint

        if n == max_iter:
            _log.info("Max iteration reached and no stable changepoint found.")
            stable_changepoint = False
        else:
            stable_changepoint = True
        # llr in interest window
        if interest_window is None:
            llr_int = np.inf
            pval_int = np.NaN
            delta_int = None
        else:
            # need to re-calculating mu0 and mu1 after the while loop
            mu0 = np.mean(ts_int[: (changepoint + 1)])
            mu1 = np.mean(ts_int[(changepoint + 1) :])

            llr_int = self._get_llr(ts_int, mu0, mu1, changepoint)
            pval_int = 1 - chi2.cdf(llr_int, 2)
            delta_int = mu1 - mu0
            changepoint += interest_window[0]
        # full time changepoint and mean
        # Note: here we are using whole TS
        mu0 = np.mean(ts[: (changepoint + 1)])
        mu1 = np.mean(ts[(changepoint + 1) :])

        return CUSUMChangePointVal(
            changepoint=changepoint,
            mu0=mu0,
            mu1=mu1,
            changetime=self.data.time[changepoint],
            stable_changepoint=stable_changepoint,
            delta=mu1 - mu0,
            llr_int=llr_int,
            p_value_int=pval_int,
            delta_int=delta_int,
        )

    def _get_llr(
        self,
        ts: np.ndarray,
        mu0: float,
        mu1: float,
        changepoint: int,
    ) -> float:
        """Calculate the log likelihood ratio."""
        scale = np.sqrt(
            (
                np.sum((ts[: (changepoint + 1)] - mu0) ** 2)
                + np.sum((ts[(changepoint + 1) :] - mu1) ** 2)
            )
            / (len(ts) - 2)
        )
        mu_tilde, sigma_tilde = np.mean(ts), np.std(ts)

        if scale == 0:
            scale = sigma_tilde * 0.01

        llr = -2 * (
            self._log_llr(ts[: (changepoint + 1)], mu_tilde, sigma_tilde, mu0, scale)
            + self._log_llr(ts[(changepoint + 1) :], mu_tilde, sigma_tilde, mu1, scale)
        )
        return llr

    def _log_llr(
        self, x: np.ndarray, mu0: float, sigma0: float, mu1: float, sigma1: float
    ) -> float:
        """Helper function to calculate log likelihood ratio.

        This function calculate the log likelihood ratio of two Gaussian
        distribution log(l(0)/l(1)).

        Args:
            x: the data value.
            mu0: mean of model 0.
            sigma0: std of model 0.
            mu1: mean of model 1.
            sigma1: std of model 1.

        Returns:
            the value of log likelihood ratio.
        """
        return np.sum(
            np.log(sigma1 / sigma0)
            + 0.5 * (((x - mu1) / sigma1) ** 2 - ((x - mu0) / sigma0) ** 2)
        )

    def _magnitude_compare(self, ts: np.ndarray) -> float:
        """Compare daily magnitude to avoid daily seasonality false positives."""
        time = self.data.time
        interest_window = self.interest_window
        magnitude_ratio = self.magnitude_ratio
        if interest_window is None:
            raise ValueError("detect must be called first")
        assert magnitude_ratio is not None
        # get number of days in historical window
        days = (time.max() - time.min()).days
        # get interest window magnitude
        mag_int = self._get_time_series_magnitude(
            ts[interest_window[0] : interest_window[1]]
        )

        comparable_mag = 0

        for i in range(days):
            start_time = time[interest_window[0]] - pd.Timedelta(f"{i}D")
            end_time = time[interest_window[1]] - pd.Timedelta(f"{i}D")
            start_idx = time[time == start_time].index[0]
            end_idx = time[time == end_time].index[0]

            hist_int = self._get_time_series_magnitude(ts[start_idx:end_idx])
            if mag_int / hist_int >= magnitude_ratio:
                comparable_mag += 1

        return comparable_mag / days

    def _get_time_series_magnitude(self, ts: np.ndarray) -> float:
        """Calculate the magnitude of a time series."""
        magnitude = np.quantile(ts, self.magnitude_quantile, interpolation="nearest")
        return magnitude

    # pyre-fixme[14]: `detector` overrides method defined in `Detector` inconsistently.
    def detector(self, **kwargs: Any) -> Sequence[CUSUMChangePoint]:
        """Find the change point and calculate related statistics.

        Args:
            threshold: Optional; float; significance level, default: 0.01.
            max_iter: Optional; int, maximum iteration in finding the
                changepoint.
            delta_std_ratio: Optional; float; the mean delta have to larger than
                this parameter times std of the data to be consider as a change.
            min_abs_change: Optional; int; minimal absolute delta between mu0
                and mu1.
            start_point: Optional; int; the start idx of the changepoint, if
                None means the middle of the time series.
            change_directions: Optional; list<str>; a list contain either or
                both 'increase' and 'decrease' to specify what type of change
                want to detect, to point both directions can be also setted up
                as empty list ([]), None or ["both"]
            interest_window: Optional; list<int, int>, a list containing the
                start and end of interest windows where we will look for change
                points. Note that llr will still be calculated using all data
                points.
            magnitude_quantile: Optional; float; the quantile for magnitude
                comparison, if none, will skip the magnitude comparison.
            magnitude_ratio: Optional; float; comparable ratio.
            magnitude_comparable_day: Optional; float; maximal percentage of
                days can have comparable magnitude to be considered as
                regression.
            return_all_changepoints: Optional; bool; return all the changepoints
                found, even the insignificant ones.

        Returns:
            A list of CUSUMChangePoint.
        """
        defaultArgs = CUSUMDefaultArgs()
        # Extract all arg values or assign defaults from default vals constant
        threshold = kwargs.get("threshold", defaultArgs.threshold)
        max_iter = kwargs.get("max_iter", defaultArgs.max_iter)
        delta_std_ratio = kwargs.get("delta_std_ratio", defaultArgs.delta_std_ratio)
        min_abs_change = kwargs.get("min_abs_change", defaultArgs.min_abs_change)
        start_point = kwargs.get("start_point", defaultArgs.start_point)
        change_directions = kwargs.get(
            "change_directions", defaultArgs.change_directions
        )
        interest_window = kwargs.get("interest_window", defaultArgs.interest_window)
        magnitude_quantile = kwargs.get(
            "magnitude_quantile", defaultArgs.magnitude_quantile
        )
        magnitude_ratio = kwargs.get("magnitude_ratio", defaultArgs.magnitude_ratio)
        magnitude_comparable_day = kwargs.get(
            "magnitude_comparable_day", defaultArgs.magnitude_comparable_day
        )
        return_all_changepoints = kwargs.get(
            "return_all_changepoints", defaultArgs.return_all_changepoints
        )

        self.interest_window = interest_window
        self.magnitude_quantile = magnitude_quantile
        self.magnitude_ratio = magnitude_ratio
        # Use array to store the data
        ts = self.data.value.to_numpy()
        ts = ts.astype("float64")
        changes_meta = {}
        if type(change_directions) is str:
            change_directions = [change_directions]

        if (
            change_directions is None
            or change_directions == [""]
            or change_directions == ["both"]
            or change_directions == []
        ):
            change_directions = ["increase", "decrease"]

        for change_direction in change_directions:
            if change_direction not in {"increase", "decrease"}:
                raise ValueError(
                    "Change direction must be 'increase' or 'decrease.' "
                    f"Got {change_direction}"
                )

            change_meta = self._get_change_point(
                ts,
                max_iter=max_iter,
                start_point=start_point,
                change_direction=change_direction,
            )
            change_meta.llr = llr = self._get_llr(
                ts,
                change_meta.mu0,
                change_meta.mu1,
                change_meta.changepoint,
            )
            change_meta.p_value = 1 - chi2.cdf(llr, 2)
            # compare magnitude on interest_window and historical_window
            if np.min(ts) >= 0:
                if magnitude_quantile and interest_window:
                    change_ts = ts if change_direction == "increase" else -ts
                    mag_change = (
                        self._magnitude_compare(change_ts) >= magnitude_comparable_day
                    )
                else:
                    mag_change = True
            else:
                mag_change = True
                if magnitude_quantile:
                    _log.warning(
                        (
                            "The minimal value is less than 0. Cannot perform "
                            "magnitude comparison."
                        )
                    )

            if_significant = llr > chi2.ppf(1 - threshold, 2)
            if_significant_int = change_meta.llr_int > chi2.ppf(1 - threshold, 2)
            if change_direction == "increase":
                larger_than_min_abs_change = (
                    change_meta.mu0 + min_abs_change < change_meta.mu1
                )
            else:
                larger_than_min_abs_change = (
                    change_meta.mu0 > change_meta.mu1 + min_abs_change
                )
            larger_than_std = (
                np.abs(change_meta.delta)
                > np.std(ts[: change_meta.changepoint]) * delta_std_ratio
            )

            change_meta.regression_detected = (
                if_significant
                and if_significant_int
                and larger_than_min_abs_change
                and larger_than_std
                and mag_change
            )
            changes_meta[change_direction] = asdict(change_meta)

        self.changes_meta = changes_meta

        return self._convert_cusum_changepoints(changes_meta, return_all_changepoints)

    def _convert_cusum_changepoints(
        self,
        cusum_changepoints: Dict[str, Dict[str, Any]],
        return_all_changepoints: bool,
    ) -> List[CUSUMChangePoint]:
        """Convert the output from the other ts cusum algorithm into CUSUMChangePoint type."""
        converted = []
        detected_cps = cusum_changepoints

        for direction in detected_cps:
            dir_cps = detected_cps[direction]
            if dir_cps["regression_detected"] or return_all_changepoints:
                # we have a change point
                change_point = CUSUMChangePoint(
                    start_time=dir_cps["changetime"],
                    end_time=dir_cps["changetime"],
                    confidence=1 - dir_cps["p_value"],
                    direction=direction,
                    cp_index=dir_cps["changepoint"],
                    mu0=dir_cps["mu0"],
                    mu1=dir_cps["mu1"],
                    delta=dir_cps["delta"],
                    llr_int=dir_cps["llr_int"],
                    llr=dir_cps["llr"],
                    regression_detected=dir_cps["regression_detected"],
                    stable_changepoint=dir_cps["stable_changepoint"],
                    p_value=dir_cps["p_value"],
                    p_value_int=dir_cps["p_value_int"],
                )
                converted.append(change_point)

        return converted

    # pyre-fixme[14]: `plot` overrides method defined in `Detector` inconsistently.
    def plot(
        self, change_points: Sequence[CUSUMChangePoint], **kwargs: Any
    ) -> plt.Axes:
        """Plot detection results from CUSUM.

        Args:
            change_points: A list of CUSUMChangePoint.
            kwargs: other arguments to pass to subplots.

        Returns:
            The matplotlib Axes.
        """
        time_col_name = self.data.time.name
        val_col_name = self.data.value.name

        data_df = self.data.to_dataframe()

        _, ax = plt.subplots(**kwargs)
        ax.plot(data_df[time_col_name], data_df[val_col_name])

        changepoint_annotated = False
        for change in change_points:
            if change.regression_detected:
                ax.axvline(x=change.start_time, color="red")
                changepoint_annotated = True
        if not changepoint_annotated:
            _log.warning("No change points detected!")

        interest_window = self.interest_window
        if interest_window is not None:
            ax.axvspan(
                pd.to_datetime(self.data.time)[interest_window[0]],
                pd.to_datetime(self.data.time)[interest_window[1] - 1],
                alpha=0.3,
                label="interets_window",
            )

        return ax


class MultiCUSUMDetector(CUSUMDetector):
    """MultiCUSUM is similar to univariate CUSUM.

    The detector is used to detect changepoints in the multivariate mean of the time series.
    The cusum values and likelihood ratio test calculations assume the underlying distribution
    has a Multivariate Guassian distriubtion.

    Attributes:
        data: The input time series data from TimeSeriesData
    """

    def __init__(self, data: TimeSeriesData) -> None:
        super(MultiCUSUMDetector, self).__init__(data=data, is_multivariate=True)

    def detector(self, **kwargs: Any) -> List[CUSUMChangePoint]:
        """Overwrite the detector method for MultiCUSUMDetector.

        Args:
            threshold: Optional; float; significance level, default: 0.01.
            max_iter: Optional; int, maximum iteration in finding the
                changepoint.
            start_point: Optional; int; the start idx of the changepoint, if
                None means the middle of the time series.
        """
        defaultArgs = CUSUMDefaultArgs()
        # Extract all arg values or assign defaults from default vals constant
        threshold = kwargs.get("threshold", defaultArgs.threshold)
        max_iter = kwargs.get("max_iter", defaultArgs.max_iter)
        start_point = kwargs.get("start_point", defaultArgs.start_point)
        # TODO: Add support for interest windows
        return_all_changepoints = kwargs.get(
            "return_all_changepoints", defaultArgs.return_all_changepoints
        )
        # Use array to store the data
        ts = self.data.value.to_numpy()
        ts = ts.astype("float64")
        changes_meta = {}
        # We will always be looking for increases in the CUSUM values for
        # multivariate detection. We keep using change_direction = "increase"
        # here to be consistent with the univariate detector.
        for change_direction in ["increase"]:

            change_meta = self._get_change_point(
                ts,
                max_iter=max_iter,
                start_point=start_point,
            )
            change_meta.llr = llr = self._get_llr(
                ts,
                change_meta.mu0,
                change_meta.mu1,
                change_meta.changepoint,
                change_meta.sigma0,
                change_meta.sigma1,
            )
            change_meta.p_value = 1 - chi2.cdf(llr, ts.shape[1] + 1)

            if_significant = llr > chi2.ppf(1 - threshold, ts.shape[1] + 1)

            change_meta.regression_detected = if_significant
            changes_meta[change_direction] = asdict(change_meta)

        self.changes_meta = changes_meta

        return self._convert_cusum_changepoints(changes_meta, return_all_changepoints)

    # pyre-fixme[14]: `_get_llr` overrides method defined in `CUSUMDetector`
    #  inconsistently.
    def _get_llr(
        self,
        ts: np.ndarray,
        mu0: float,
        mu1: float,
        changepoint: int,
        sigma0: Optional[float],
        sigma1: Optional[float],
    ) -> float:

        mu_tilde = np.mean(ts, axis=0)
        sigma_pooled = np.cov(ts, rowvar=False)
        llr = -2 * (
            self._log_llr_multi(
                ts[: (changepoint + 1)],
                mu_tilde,
                sigma_pooled,
                mu0,
                sigma0,
            )
            - self._log_llr_multi(
                ts[(changepoint + 1) :],
                mu_tilde,
                sigma_pooled,
                mu1,
                sigma1,
            )
        )
        return llr

    def _log_llr_multi(
        self,
        x: np.ndarray,
        mu0: Union[float, np.ndarray],
        sigma0: Union[float, np.ndarray],
        mu1: Union[float, np.ndarray],
        sigma1: Union[float, np.ndarray],
    ) -> float:
        try:
            sigma0_inverse = np.linalg.inv(sigma0)
            sigma1_inverse = np.linalg.inv(sigma1)
            log_det_sigma0 = np.log(np.linalg.det(sigma0))
            log_det_sigma1 = np.log(np.linalg.det(sigma1))
        except np.linalg.linalg.LinAlgError:
            msg = "One or more covariance matrix is singular."
            _log.error(msg)
            raise ValueError(msg)

        return len(x) / 2 * (log_det_sigma0 - log_det_sigma1) + np.sum(
            -np.matmul(np.matmul(x[i] - mu1, sigma1_inverse), (x[i] - mu1).T)
            + np.matmul(np.matmul(x[i] - mu0, sigma0_inverse), (x[i] - mu0).T)
            for i in range(len(x))
        )

    def _get_change_point(
        self,
        ts: np.ndarray,
        max_iter: int,
        start_point: int,
        change_direction: str = "increase",
    ) -> CUSUMChangePointVal:
        """Locate the change point using cusum method."""
        changepoint_func = np.argmin
        n = 0
        ts_int = ts

        if start_point is None:
            start_point = len(ts_int) // 2
        changepoint = start_point
        # iterate until the changepoint converage
        while n < max_iter:
            n += 1
            data_before_changepoint = ts_int[: (changepoint + 1)]
            data_after_changepoint = ts_int[(changepoint + 1) :]

            mu0 = np.mean(data_before_changepoint, axis=0)
            mu1 = np.mean(data_after_changepoint, axis=0)
            # TODO: replace pooled variance with sample variances before and
            # after changepoint.
            # sigma0 = np.cov(data_before_changepoint, rowvar=False)
            # sigma1 = np.cov(data_after_changepoint, rowvar=False)
            sigma0 = sigma1 = np.cov(ts_int, rowvar=False)

            try:
                log_det_sigma0 = np.log(np.linalg.det(sigma0))
                log_det_sigma1 = np.log(np.linalg.det(sigma1))
                sigma0_inverse = np.linalg.inv(sigma0)
                sigma1_inverse = np.linalg.inv(sigma1)
            except np.linalg.linalg.LinAlgError:
                msg = "One or more covariance matrix is singular."
                _log.error(msg)
                raise ValueError(msg)

            si_values = np.diag(
                -(1 / 2) * log_det_sigma1
                - np.matmul(np.matmul(ts_int - mu1, sigma1_inverse), (ts_int - mu1).T)
                + (1 / 2) * log_det_sigma0
                + np.matmul(np.matmul(ts_int - mu0, sigma0_inverse), (ts_int - mu0).T)
            )

            cusum_ts = np.cumsum(si_values)
            next_changepoint = max(
                1, min(changepoint_func(cusum_ts), len(cusum_ts) - 2)
            )

            if next_changepoint == changepoint:
                break
            else:
                changepoint = next_changepoint

        if n == max_iter:
            _log.info("Max iteration reached and no stable changepoint found.")
            stable_changepoint = False
        else:
            stable_changepoint = True

        llr_int = np.inf
        pval_int = np.NaN
        delta_int = None
        # full time changepoint and mean
        mu0 = np.mean(ts[: (changepoint + 1)], axis=0)
        mu1 = np.mean(ts[(changepoint + 1) :], axis=0)
        sigma0 = sigma1 = np.cov(ts, rowvar=False)

        return CUSUMChangePointVal(
            changepoint=changepoint,
            mu0=mu0,
            mu1=mu1,
            changetime=self.data.time[changepoint],
            stable_changepoint=stable_changepoint,
            delta=mu1 - mu0,
            llr_int=llr_int,
            p_value_int=pval_int,
            delta_int=delta_int,
            sigma0=sigma0,
            sigma1=sigma1,
        )


class VectorizedCUSUMDetector(CUSUMDetector):
    """VectorizedCUSUM is the vecteorized version of CUSUM.

    It can take multiple time series as an input and run CUSUM algorithm
    on each time series in a vectorized manner.

    Attributes:
        data: The input time series data from TimeSeriesData
    """

    changes_meta_list: Optional[List[Dict[str, Dict[str, Any]]]] = None

    def __init__(self, data: TimeSeriesData) -> None:
        super(VectorizedCUSUMDetector, self).__init__(
            data=data, is_multivariate=False, is_vectorized=True
        )

    def detector(self, **kwargs: Any) -> List[List[CUSUMChangePoint]]:
        """Detector method for vectorized version of CUSUM.

        Args:
            threshold: Optional; float; significance level, default: 0.01.
            max_iter: Optional; int, maximum iteration in finding the
                changepoint.
            delta_std_ratio: Optional; float; the mean delta have to larger than
                this parameter times std of the data to be consider as a change.
            min_abs_change: Optional; int; minimal absolute delta between mu0
                and mu1.
            start_point: Optional; int; the start idx of the changepoint, if
                None means the middle of the time series.
            change_directions: Optional; list<str>; a list contain either or
                both 'increase' and 'decrease' to specify what type of change
                want to detect.
            interest_window: Optional; list<int, int>, a list containing the
                start and end of interest windows where we will look for change
                points. Note that llr will still be calculated using all data
                points.
            magnitude_quantile: Optional; float; the quantile for magnitude
                comparison, if none, will skip the magnitude comparison.
            magnitude_ratio: Optional; float; comparable ratio.
            magnitude_comparable_day: Optional; float; maximal percentage of
                days can have comparable magnitude to be considered as
                regression.
            return_all_changepoints: Optional; bool; return all the changepoints
                found, even the insignificant ones.

        Returns:
            A list of CUSUMChangePoint.
        """
        defaultArgs = CUSUMDefaultArgs()
        # Extract all arg values or assign defaults from default vals constant
        threshold = kwargs.get("threshold", defaultArgs.threshold)
        max_iter = kwargs.get("max_iter", defaultArgs.max_iter)
        delta_std_ratio = kwargs.get("delta_std_ratio", defaultArgs.delta_std_ratio)
        min_abs_change = kwargs.get("min_abs_change", defaultArgs.min_abs_change)
        start_point = kwargs.get("start_point", defaultArgs.start_point)
        change_directions = kwargs.get(
            "change_directions", defaultArgs.change_directions
        )
        interest_window = kwargs.get("interest_window", defaultArgs.interest_window)
        magnitude_quantile = kwargs.get(
            "magnitude_quantile", defaultArgs.magnitude_quantile
        )
        magnitude_ratio = kwargs.get("magnitude_ratio", defaultArgs.magnitude_ratio)
        magnitude_comparable_day = kwargs.get(
            "magnitude_comparable_day", defaultArgs.magnitude_comparable_day
        )
        return_all_changepoints = kwargs.get(
            "return_all_changepoints", defaultArgs.return_all_changepoints
        )

        self.interest_window = interest_window
        self.magnitude_quantile = magnitude_quantile
        self.magnitude_ratio = magnitude_ratio
        # Use array to store the data
        ts_multi = self.data.value.to_numpy()
        ts_multi = ts_multi.astype("float64")
        if ts_multi.ndim == 1:
            ts_multi = ts_multi[:, np.newaxis]

        changes_meta_multi = {}

        if type(change_directions) is str:
            change_directions = [change_directions]

        if (
            change_directions is None
            or change_directions == [""]
            or change_directions == ["both"]
            or change_directions == []
        ):
            change_directions = ["increase", "decrease"]

        for change_direction in change_directions:
            if change_direction not in {"increase", "decrease"}:
                raise ValueError(
                    "Change direction must be 'increase' or 'decrease.' "
                    f"Got {change_direction}"
                )

            changes_meta_multi[change_direction] = transfer_vect_cusum_cp_to_cusum_cp(
                self._get_change_point_multiple_ts(
                    ts_multi,
                    max_iter=max_iter,
                    change_direction=change_direction,
                    start_point=start_point,
                )
            )
            for col_idx in np.arange(ts_multi.shape[1]):
                ts = ts_multi[:, col_idx]
                # current change_meta doesn't have sigma0, sigma1, llr, p_value, regression_detected
                change_meta = changes_meta_multi[change_direction][col_idx]
                change_meta.llr = llr = self._get_llr(
                    ts,
                    change_meta.mu0,
                    change_meta.mu1,
                    change_meta.changepoint,
                )
                change_meta.p_value = 1 - chi2.cdf(llr, 2)
                # compare magnitude on interest_window and historical_window
                if np.min(ts) >= 0:
                    if magnitude_quantile and interest_window:
                        change_ts = ts if change_direction == "increase" else -ts
                        mag_change = (
                            self._magnitude_compare(change_ts)
                            >= magnitude_comparable_day
                        )
                    else:
                        mag_change = True
                else:
                    mag_change = True
                    if magnitude_quantile:
                        _log.warning(
                            (
                                "The minimal value is less than 0. Cannot perform "
                                "magnitude comparison."
                            )
                        )

                if_significant = llr > chi2.ppf(1 - threshold, 2)
                if_significant_int = change_meta.llr_int > chi2.ppf(1 - threshold, 2)
                if change_direction == "increase":
                    larger_than_min_abs_change = (
                        change_meta.mu0 + min_abs_change < change_meta.mu1
                    )
                else:
                    larger_than_min_abs_change = (
                        change_meta.mu0 > change_meta.mu1 + min_abs_change
                    )
                larger_than_std = (
                    np.abs(change_meta.delta)
                    > np.std(ts[: change_meta.changepoint]) * delta_std_ratio
                )

                change_meta.regression_detected = (
                    if_significant
                    and if_significant_int
                    and larger_than_min_abs_change
                    and larger_than_std
                    and mag_change
                )

                changes_meta_multi[change_direction][col_idx] = asdict(change_meta)

        self.changes_meta_multi = changes_meta_multi

        res = []
        for col_idx in np.arange(ts_multi.shape[1]):
            temp = {}
            for change_direction in change_directions:
                temp[change_direction] = self.changes_meta_multi[change_direction][
                    col_idx
                ]

            res.append(self._convert_cusum_changepoints(temp, return_all_changepoints))
        return res

    def detector_(self, **kwargs: Any) -> List[List[CUSUMChangePoint]]:
        """Detector method for vectorized version of CUSUM.

        Args:
            threshold: Optional; float; significance level, default: 0.01.
            max_iter: Optional; int, maximum iteration in finding the
                changepoint.
            delta_std_ratio: Optional; float; the mean delta have to larger than
                this parameter times std of the data to be consider as a change.
            min_abs_change: Optional; int; minimal absolute delta between mu0
                and mu1.
            change_directions: Optional; list<str>; a list contain either or
                both 'increase' and 'decrease' to specify what type of change
                want to detect.
            interest_window: Optional; list<int, int>, a list containing the
                start and end of interest windows where we will look for change
                points. Note that llr will still be calculated using all data
                points.
            magnitude_quantile: Optional; float; the quantile for magnitude
                comparison, if none, will skip the magnitude comparison.
            magnitude_ratio: Optional; float; comparable ratio.
            magnitude_comparable_day: Optional; float; maximal percentage of
                days can have comparable magnitude to be considered as
                regression.
            return_all_changepoints: Optional; bool; return all the changepoints
                found, even the insignificant ones.

        Returns:
            A list of tuple of TimeSeriesChangePoint and CUSUMMetadata.
        """
        defaultArgs = CUSUMDefaultArgs()
        # Extract all arg values or assign defaults from default vals constant
        threshold = kwargs.get("threshold", defaultArgs.threshold)
        max_iter = kwargs.get("max_iter", defaultArgs.max_iter)
        delta_std_ratio = kwargs.get("delta_std_ratio", defaultArgs.delta_std_ratio)
        min_abs_change = kwargs.get("min_abs_change", defaultArgs.min_abs_change)
        change_directions = kwargs.get(
            "change_directions", defaultArgs.change_directions
        )
        interest_window = kwargs.get("interest_window", defaultArgs.interest_window)
        magnitude_quantile = kwargs.get(
            "magnitude_quantile", defaultArgs.magnitude_quantile
        )
        magnitude_ratio = kwargs.get("magnitude_ratio", defaultArgs.magnitude_ratio)
        magnitude_comparable_day = kwargs.get(
            "magnitude_comparable_day", defaultArgs.magnitude_comparable_day
        )
        return_all_changepoints = kwargs.get(
            "return_all_changepoints", defaultArgs.return_all_changepoints
        )
        self.interest_window = interest_window
        self.magnitude_quantile = magnitude_quantile
        self.magnitude_ratio = magnitude_ratio
        # Use array to store the data
        ts_all = self.data.value.to_numpy()
        ts_all = ts_all.astype("float64")
        if ts_all.ndim == 1:
            ts_all = ts_all[:, np.newaxis]
        changes_meta_list = []

        if change_directions is None:
            change_directions = ["increase", "decrease"]

        change_meta_all = {}
        for change_direction in change_directions:
            if change_direction not in {"increase", "decrease"}:
                raise ValueError(
                    "Change direction must be 'increase' or 'decrease.' "
                    f"Got {change_direction}"
                )

            change_meta_all[change_direction] = asdict(
                self._get_change_point_multiple_ts(
                    ts_all,
                    max_iter=max_iter,
                    change_direction=change_direction,
                )
            )

        ret = []
        for col_idx in np.arange(ts_all.shape[1]):
            ts = ts_all[:, col_idx]
            changes_meta = {}
            for change_direction in change_directions:
                change_meta_ = change_meta_all[change_direction]
                # if no change points are detected, skip
                if not list(change_meta_["changepoint"]):
                    continue
                change_meta = {
                    k: (
                        change_meta_[k][col_idx]
                        if isinstance(change_meta_[k], np.ndarray)
                        or isinstance(change_meta_[k], list)
                        else change_meta_[k]
                    )
                    for k in change_meta_
                }
                change_meta["llr"] = llr = self._get_llr(
                    ts,
                    change_meta["mu0"],
                    change_meta["mu1"],
                    change_meta["changepoint"],
                )
                change_meta["p_value"] = 1 - chi2.cdf(change_meta["llr"], 2)
                # compare magnitude on interest_window and historical_window
                if np.min(ts) >= 0:
                    if magnitude_quantile and interest_window:
                        change_ts = ts if change_direction == "increase" else -ts
                        mag_change = (
                            self._magnitude_compare(change_ts)
                            >= magnitude_comparable_day
                        )
                    else:
                        mag_change = True
                else:
                    mag_change = True
                    if magnitude_quantile:
                        _log.warning(
                            (
                                "The minimal value is less than 0. Cannot perform "
                                "magnitude comparison."
                            )
                        )

                if_significant = llr > chi2.ppf(1 - threshold, 2)
                if_significant_int = change_meta["llr_int"] > chi2.ppf(1 - threshold, 2)
                if change_direction == "increase":
                    larger_than_min_abs_change = (
                        change_meta["mu0"] + min_abs_change < change_meta["mu1"]
                    )
                else:
                    larger_than_min_abs_change = (
                        change_meta["mu0"] > change_meta["mu1"] + min_abs_change
                    )
                larger_than_std = (
                    np.abs(change_meta["delta"])
                    > np.std(ts[: change_meta["changepoint"]]) * delta_std_ratio
                )

                change_meta["regression_detected"] = (
                    if_significant
                    and if_significant_int
                    and larger_than_min_abs_change
                    and larger_than_std
                    and mag_change
                )

                changes_meta[change_direction] = change_meta
            changes_meta_list.append(changes_meta)
            ret.append(
                self._convert_cusum_changepoints(changes_meta, return_all_changepoints)
            )
        self.changes_meta_list = changes_meta_list
        return ret

    def _get_change_point_multiple_ts(
        self,
        ts: np.ndarray,
        max_iter: int,
        change_direction: str,
        start_point: Optional[int] = None,
    ) -> VectorizedCUSUMChangePointVal:
        """Find change points in a list of time series."""
        interest_window = self.interest_window
        # locate the change point using cusum method
        if change_direction == "increase":
            changepoint_func = np.argmin
            _log.debug("Detecting increase changepoint.")
        else:
            assert change_direction == "decrease"
            changepoint_func = np.argmax
            _log.debug("Detecting decrease changepoint.")

        if interest_window is not None:
            ts_int = ts[interest_window[0] : interest_window[1], :]
        else:
            ts_int = ts

        n_ts = ts_int.shape[1]
        n_pts = ts_int.shape[0]
        # corner case
        if n_pts == 0:
            return VectorizedCUSUMChangePointVal(
                changepoint=[],
                mu0=[],
                mu1=[],
                changetime=[],
                stable_changepoint=[],
                delta=[],
                llr_int=[],
                p_value_int=[],
                delta_int=[],
            )
        # use the middle point as initial change point to estimate mu0 and mu1
        tmp = ts_int - np.tile(np.mean(ts_int, axis=0), (n_pts, 1))
        cusum_ts = np.cumsum(tmp, axis=0)
        if start_point is not None:
            changepoint = np.asarray([start_point] * n_ts)
        else:
            changepoint = np.minimum(changepoint_func(cusum_ts, axis=0), n_pts - 2)
        # iterate until the changepoint converage
        mu0 = mu1 = None
        stable_changepoint = [False] * len(changepoint)
        n = 0
        while n < max_iter:
            mask = np.zeros((n_pts, n_ts), dtype=bool)
            for i, c in enumerate(changepoint):
                mask[: (c + 1), i] = True
            n += 1
            mu0 = np.divide(
                np.sum(np.multiply(ts_int, mask), axis=0), np.sum(mask, axis=0)
            )
            mu1 = np.divide(
                np.sum(np.multiply(ts_int, ~mask), axis=0), np.sum(~mask, axis=0)
            )
            mean = (mu0 + mu1) / 2
            # here is where cusum is happening
            tmp = ts_int - np.tile(mean, (n_pts, 1))
            cusum_ts = np.cumsum(tmp, axis=0)
            next_changepoint = np.maximum(
                np.minimum(changepoint_func(cusum_ts, axis=0), n_pts - 2), 1
            )
            stable_changepoint = np.equal(changepoint, next_changepoint)
            if all(stable_changepoint):
                break
            changepoint = next_changepoint
        # need to re-calculating mu0 and mu1 after the while loop
        mask = np.zeros(ts_int.shape, dtype=bool)
        for i, c in enumerate(changepoint):
            mask[: (c + 1), i] = True
        mu0 = np.divide(np.sum(np.multiply(ts_int, mask), axis=0), np.sum(mask, axis=0))
        mu1 = np.divide(
            np.sum(np.multiply(ts_int, ~mask), axis=0), np.sum(~mask, axis=0)
        )
        # llr in interest window
        if interest_window is None:
            llr_int = [np.inf] * n_ts
            pval_int = [np.NaN] * n_ts
            delta_int = [None] * n_ts
        else:
            llr_int = []
            pval_int = []
            delta_int = []
            for col_idx in np.arange(n_ts):
                _llr_int = self._get_llr(
                    ts_int[:, col_idx], mu0[col_idx], mu1[col_idx], changepoint[col_idx]
                )
                _pval_int = 1 - chi2.cdf(_llr_int, 2)
                _delta_int = mu1[col_idx] - mu0[col_idx]
                llr_int.append(_llr_int)
                pval_int.append(_pval_int)
                delta_int.append(_delta_int)
                changepoint[col_idx] += interest_window[0]
        # full time changepoint and mean
        # Note: here we are using whole TS
        mask = np.zeros(ts.shape, dtype=bool)
        for i, c in enumerate(changepoint):
            mask[: (c + 1), i] = True
        mu0 = np.divide(np.sum(np.multiply(ts, mask), axis=0), np.sum(mask, axis=0))
        mu1 = np.divide(np.sum(np.multiply(ts, ~mask), axis=0), np.sum(~mask, axis=0))

        return VectorizedCUSUMChangePointVal(
            changepoint=changepoint,
            mu0=mu0,
            mu1=mu1,
            changetime=[self.data.time[c] for c in changepoint],
            stable_changepoint=stable_changepoint,
            delta=mu1 - mu0,
            llr_int=llr_int,
            p_value_int=pval_int,
            delta_int=delta_int,
        )


def percentage_change(
    data: TimeSeriesData, pre_mean: Union[float, pd.Series], **kwargs: Any
) -> TimeSeriesData:
    """Calculate percentage change absolute change / baseline change.

    Args:
        data: The data need to calculate the score
        pre_mean: Baseline mean
    """
    if isinstance(data.value, pd.DataFrame) and data.value.shape[1] > 1:
        res = (data.value - pre_mean) / (pre_mean)
        return TimeSeriesData(value=res, time=data.time)
    else:
        return (data - pre_mean) / (pre_mean)


def change(
    data: TimeSeriesData, pre_mean: Union[float, pd.Series], **kwargs: Any
) -> TimeSeriesData:
    """Calculate absolute change.

    Args:
        data: The data need to calculate the score
        pre_mean: Baseline mean
    """
    if isinstance(data.value, pd.DataFrame) and data.value.shape[1] > 1:
        res = data.value - pre_mean
        return TimeSeriesData(value=res, time=data.time)
    else:
        return data - pre_mean


def z_score(
    data: TimeSeriesData,
    pre_mean: Union[float, pd.Series],
    pre_std: Union[float, pd.Series],
) -> TimeSeriesData:
    """Calculate z score.

    The formula for calculating a z-score is is z = (x-mu)/sigma,
    where x is the raw score, mu is the population mean,
    and sigma is the population standard deviation.

    population standard deviation -> ddof = 0

    Args:
        data: The data need to calculate the score
        pre_mean: Baseline mean
        pre_std: Baseline std
    """
    if isinstance(data.value, pd.DataFrame) and data.value.shape[1] > 1:
        res = (data.value - pre_mean) / (pre_std)
        return TimeSeriesData(value=res, time=data.time)
    else:
        return (data - pre_mean) / (pre_std)


class CusumScoreFunction(Enum):
    """Cusum score function."""

    change = "change"
    percentage_change = "percentage_change"
    z_score = "z_score"


# Score Function Constants
SCORE_FUNC_DICT = {
    CusumScoreFunction.change.value: change,
    CusumScoreFunction.percentage_change.value: percentage_change,
    CusumScoreFunction.z_score.value: z_score,
}
DEFAULT_SCORE_FUNCTION: CusumScoreFunction = CusumScoreFunction.change
STR_TO_SCORE_FUNC: Dict[str, CusumScoreFunction] = {  # Used for param tuning
    "change": CusumScoreFunction.change,
    "percentage_change": CusumScoreFunction.percentage_change,
    "z_score": CusumScoreFunction.z_score,
}


class PredictFunctionValues(NamedTuple):
    """Predict function values."""

    score: TimeSeriesData
    absolute_change: TimeSeriesData


class CUSUMDetectorModel(DetectorModel):
    """CUSUMDetectorModel for detecting multiple level shift change points.

    CUSUMDetectorModel runs CUSUMDetector multiple times to detect multiple change
    points. In each run, CUSUMDetector will use historical_window + scan_window as
    input time series, and find change point in scan_window. The DetectorModel stores
    change points and returns anomaly score.

    Attributes:
        cps: Change points detected in unixtime.
        alert_fired: If a change point is detected and the anomaly still present.
        pre_mean: Previous baseline mean.
        pre_std: Previous baseline std.
        number_of_normal_scan: Number of scans with mean returned back to baseline.
        alert_change_direction: Increase or decrease.
        scan_window: Length in seconds of scan window.
        historical_window: Length in seconds of historical window.
        step_window: The time difference between CUSUM runs.
        threshold: CUSUMDetector threshold.
        delta_std_ratio: The mean delta have to larger than this parameter times std of
            the data to be consider as a change.
        magnitude_quantile: See in CUSUMDetector.
        magnitude_ratio: See in CUSUMDetector.
        score_func: The score function to calculate the anomaly score.
        remove_seasonality: If apply STL to remove seasonality.
        season_period_freq: str, "daily"/"weekly"/"monthly"/"yearly"
        vectorized: bool, transfer to multi-ts and call vectorized cusum model
        adapted_pre_mean: bool, whether using a rolling pre-mean and pre-std when calculating
            anomaly scores (when alert_fired = True)
    """

    def __init__(
        self,
        serialized_model: Optional[bytes] = None,
        scan_window: Optional[int] = None,
        historical_window: Optional[int] = None,
        step_window: Optional[int] = None,
        threshold: float = CUSUMDefaultArgs.threshold,
        delta_std_ratio: float = CUSUMDefaultArgs.delta_std_ratio,
        magnitude_quantile: Optional[float] = CUSUMDefaultArgs.magnitude_quantile,
        magnitude_ratio: float = CUSUMDefaultArgs.magnitude_ratio,
        change_directions: Optional[
            Union[List[str], str]
        ] = CUSUMDefaultArgs.change_directions,
        score_func: Union[str, CusumScoreFunction] = DEFAULT_SCORE_FUNCTION,
        remove_seasonality: bool = CUSUMDefaultArgs.remove_seasonality,
        season_period_freq: Union[str, int] = "daily",
        vectorized: Optional[bool] = None,
        adapted_pre_mean: Optional[bool] = None,
    ) -> None:
        if serialized_model:
            previous_model = json.loads(serialized_model)
            self.cps: List[int] = previous_model["cps"]
            self.alert_fired: bool = previous_model["alert_fired"]
            self.pre_mean: float = previous_model["pre_mean"]
            self.pre_std: float = previous_model["pre_std"]
            self.number_of_normal_scan: int = previous_model["number_of_normal_scan"]
            self.alert_change_direction: str = previous_model["alert_change_direction"]
            self.scan_window: int = previous_model["scan_window"]
            scan_window = previous_model["scan_window"]
            self.historical_window: int = previous_model["historical_window"]
            self.step_window: int = previous_model["step_window"]
            step_window = previous_model["step_window"]
            self.threshold: float = previous_model["threshold"]
            self.delta_std_ratio: float = previous_model["delta_std_ratio"]
            self.magnitude_quantile: Optional[float] = previous_model[
                "magnitude_quantile"
            ]
            self.magnitude_ratio: float = previous_model["magnitude_ratio"]
            self.change_directions: Optional[List[str]] = previous_model[
                "change_directions"
            ]
            self.score_func: CusumScoreFunction = previous_model["score_func"]
            if "remove_seasonality" in previous_model:
                self.remove_seasonality: bool = previous_model["remove_seasonality"]
            else:
                self.remove_seasonality: bool = remove_seasonality

            self.season_period_freq: Union[str, int] = previous_model.get(
                "season_period_freq", "daily"
            )
            # If vectorized is provided, it should supersede existing values
            if vectorized is not None:
                self.vectorized: bool = vectorized
            else:
                self.vectorized: bool = previous_model.get("vectorized", False)
            # If adapted_pre_mean is provided, it should supersede existing values
            if adapted_pre_mean is not None:
                self.adapted_pre_mean: bool = adapted_pre_mean
            else:
                self.adapted_pre_mean: bool = previous_model.get(
                    "adapted_pre_mean", False
                )

        elif scan_window is not None and historical_window is not None:
            self.cps = []
            self.alert_fired = False
            self.pre_mean = 0
            self.pre_std = 1
            self.number_of_normal_scan = 0
            self.alert_change_direction: Union[str, None] = None
            self.scan_window = scan_window
            self.historical_window = historical_window
            self.step_window = cast(int, step_window)
            self.threshold = threshold
            self.delta_std_ratio = delta_std_ratio
            self.magnitude_quantile = magnitude_quantile
            self.magnitude_ratio = magnitude_ratio

            if isinstance(change_directions, str):
                self.change_directions = [change_directions]
            else:
                # List[str]
                self.change_directions = change_directions

            self.remove_seasonality = remove_seasonality
            self.season_period_freq = season_period_freq
            # We allow score_function to be a str for compatibility with param tuning
            if isinstance(score_func, str):
                if score_func in STR_TO_SCORE_FUNC:
                    score_func = STR_TO_SCORE_FUNC[score_func]
                else:
                    score_func = DEFAULT_SCORE_FUNCTION
            self.score_func = score_func.value

            self.vectorized: bool = vectorized or False
            self.adapted_pre_mean: bool = adapted_pre_mean or False

        else:
            raise ParameterError(
                "You must provide either serialized model or values for "
                "scan_window and historical_window."
            )

        self.vectorized_trans_flag: bool = False

    def __eq__(self, other: object) -> bool:
        if isinstance(other, CUSUMDetectorModel):
            return (
                self.cps == other.cps
                and self.alert_fired == other.alert_fired
                and self.pre_mean == other.pre_mean
                and self.pre_std == other.pre_std
                and self.number_of_normal_scan == other.number_of_normal_scan
                and self.alert_change_direction == other.alert_change_direction
                and self.scan_window == other.scan_window
                and self.historical_window == other.historical_window
                and self.step_window == other.step_window
                and self.threshold == other.threshold
                and self.delta_std_ratio == other.delta_std_ratio
                and self.magnitude_quantile == other.magnitude_quantile
                and self.magnitude_ratio == other.magnitude_ratio
                and self.change_directions == other.change_directions
                and self.score_func == other.score_func
            )
        return False

    def serialize(self) -> bytes:
        """Returns serilized model."""
        return str.encode(json.dumps(self.__dict__))

    def _set_alert_off(self) -> None:
        """Set alert off."""
        self.alert_fired = False
        self.number_of_normal_scan = 0

    def _set_alert_on(
        self, baseline_mean: float, baseline_std: float, alert_change_direction: str
    ) -> None:
        """Set alert on."""
        self.alert_fired = True
        self.alert_change_direction = alert_change_direction
        self.pre_mean = baseline_mean
        self.pre_std = baseline_std

    def _if_normal(
        self,
        cur_mean: float,
        change_directions: Optional[List[str]],
        delta_std_ratio: float = CUSUMDefaultArgs.delta_std_ratio,
    ) -> bool:
        if change_directions is not None:
            increase, decrease = (
                "increase" in change_directions,
                "decrease" in change_directions,
            )
        else:
            increase, decrease = True, True

        if self.alert_change_direction == "increase":
            check_increase = 0 if increase else np.inf
            check_decrease = delta_std_ratio if decrease else np.inf
        elif self.alert_change_direction == "decrease":
            check_increase = delta_std_ratio if increase else np.inf
            check_decrease = 0 if decrease else np.inf

        return (
            # pyre-fixme[61]: `check_decrease` is undefined, or not always defined.
            self.pre_mean - check_decrease * self.pre_std
            <= cur_mean
            # pyre-fixme[61]: `check_increase` is undefined, or not always defined.
            <= self.pre_mean + check_increase * self.pre_std
        )

    def _fit_vec_row(
        self,
        vec_data_row: TimeSeriesData,
        # pyre-fixme[11]: Annotation `Timedelta` is not defined as a type.
        scan_window: Union[int, pd.Timedelta],
        changepoints: List[CUSUMChangePoint],  # len = 1 or 0
        time_adjust: pd.Timedelta,
        change_directions: Optional[List[str]] = CUSUMDefaultArgs.change_directions,
        delta_std_ratio: float = CUSUMDefaultArgs.delta_std_ratio,
    ) -> List[int]:
        scan_start_time = vec_data_row.time.iloc[-1] - pd.Timedelta(
            scan_window, unit="s"
        )
        scan_start_index = max(
            0, np.argwhere((vec_data_row.time >= scan_start_time).values).min()
        )
        # need to update vec_cusum.cps
        res_cp = []
        if not self.alert_fired:
            if len(changepoints) > 0:
                cp = changepoints[0]
                self.cps.append((cp.start_time + time_adjust).value // 10**9)
                res_cp.append(cp.start_time.value // 10**9)
                if len(self.cps) > MAX_CHANGEPOINT:
                    self.cps.pop(0)

                self._set_alert_on(
                    vec_data_row.value[: cp.cp_index + 1].mean(),
                    # Note: std() from Pandas has default ddof=1, while std() from numpy has default ddof=0
                    vec_data_row.value[: cp.cp_index + 1].std(ddof=0),
                    cp.direction,
                )
        else:
            cur_mean = vec_data_row[scan_start_index:].value.mean()

            if self.adapted_pre_mean:
                self.pre_mean = vec_data_row.value[:scan_start_index].mean()
                self.pre_std = vec_data_row.value[:scan_start_index].std(ddof=0)

            if self._if_normal(cur_mean, change_directions, delta_std_ratio):
                self.number_of_normal_scan += 1
                if self.number_of_normal_scan >= NORMAL_TOLERENCE:
                    self._set_alert_off()
            else:
                self.number_of_normal_scan = 0

            current_time = int((vec_data_row.time.max() + time_adjust).value / 1e9)
            if current_time - self.cps[-1] > CHANGEPOINT_RETENTION:
                self._set_alert_off()

        return res_cp

    def _fit(
        self,
        data: TimeSeriesData,
        historical_data: TimeSeriesData,
        scan_window: Union[int, pd.Timedelta],
        threshold: float = CUSUMDefaultArgs.threshold,
        delta_std_ratio: float = CUSUMDefaultArgs.delta_std_ratio,
        magnitude_quantile: Optional[float] = CUSUMDefaultArgs.magnitude_quantile,
        magnitude_ratio: float = CUSUMDefaultArgs.magnitude_ratio,
        change_directions: Optional[List[str]] = CUSUMDefaultArgs.change_directions,
    ) -> None:
        """Fit CUSUM model.

        Args:
            data: the new data the model never seen
            historical_data: the historical data, `historical_data` have to end with the
                datapoint right before the first data point in `data`
            scan_window: scan window length in seconds, scan window is the window where
                cusum search for changepoint(s)
            threshold: changepoint significant level, higher the value more changepoints
                detected
            delta_std_ratio: the mean change have to larger than `delta_std_ratio` *
            `std(data[:changepoint])` to be consider as a change, higher the value
            less changepoints detected
            magnitude_quantile: float, the quantile for magnitude comparison, if
                none, will skip the magnitude comparison;
            magnitude_ratio: float, comparable ratio;
            change_directions: a list contain either or both 'increase' and 'decrease' to
                specify what type of change to detect;
        """
        historical_data.extend(data, validate=False)
        n = len(historical_data)
        scan_start_time = historical_data.time.iloc[-1] - pd.Timedelta(
            scan_window, unit="s"
        )
        scan_start_index = max(
            0, np.argwhere((historical_data.time >= scan_start_time).values).min()
        )

        if not self.alert_fired:
            # if scan window is less than 2 data poins and there is no alert fired
            # skip this scan
            if n - scan_start_index <= 1:
                return
            detector = CUSUMDetector(historical_data)
            changepoints = detector.detector(
                interest_window=[scan_start_index, n],
                threshold=threshold,
                delta_std_ratio=delta_std_ratio,
                magnitude_quantile=magnitude_quantile,
                magnitude_ratio=magnitude_ratio,
                change_directions=change_directions,
            )
            if len(changepoints) > 0:
                cp = sorted(changepoints, key=lambda x: x.start_time)[0]
                self.cps.append(int(cp.start_time.value / 1e9))

                if len(self.cps) > MAX_CHANGEPOINT:
                    self.cps.pop(0)

                self._set_alert_on(
                    historical_data.value[: cp.cp_index + 1].mean(),
                    # Note: std() from Pandas has default ddof=1, while std() from numpy has default ddof=0
                    historical_data.value[: cp.cp_index + 1].std(ddof=0),
                    cp.direction,
                )

        else:
            cur_mean = historical_data[scan_start_index:].value.mean()

            if self.adapted_pre_mean:
                self.pre_mean = historical_data.value[:scan_start_index].mean()
                self.pre_std = historical_data.value[:scan_start_index].std(ddof=0)

            if self._if_normal(cur_mean, change_directions, delta_std_ratio):
                self.number_of_normal_scan += 1
                if self.number_of_normal_scan >= NORMAL_TOLERENCE:
                    self._set_alert_off()
            else:
                self.number_of_normal_scan = 0

            current_time = int(data.time.max().value / 1e9)
            if current_time - self.cps[-1] > CHANGEPOINT_RETENTION:
                self._set_alert_off()

    def _predict(
        self,
        data: TimeSeriesData,
        score_func: CusumScoreFunction = CusumScoreFunction.change,
    ) -> PredictFunctionValues:
        """Performs anomaly detection."""
        if self.alert_fired:
            cp = self.cps[-1]
            tz = data.tz()
            if tz is None:
                change_time = pd.to_datetime(cp, unit="s")
            else:
                change_time = pd.to_datetime(cp, unit="s", utc=True).tz_convert(tz)

            if change_time >= data.time.iloc[0]:
                cp_index = data.time[data.time == change_time].index[0]
                data_pre = data[: cp_index + 1]
                score_pre = self._zeros_ts(data_pre)
                change_pre = self._zeros_ts(data_pre)
                score_post = SCORE_FUNC_DICT[score_func](
                    data=data[cp_index + 1 :],
                    pre_mean=self.pre_mean,
                    pre_std=self.pre_std,
                )
                score_pre.extend(score_post, validate=False)

                change_post = SCORE_FUNC_DICT[CusumScoreFunction.change.value](
                    data=data[cp_index + 1 :],
                    pre_mean=self.pre_mean,
                    pre_std=self.pre_std,
                )
                change_pre.extend(change_post, validate=False)
                return PredictFunctionValues(score_pre, change_pre)
            return PredictFunctionValues(
                SCORE_FUNC_DICT[score_func](
                    data=data, pre_mean=self.pre_mean, pre_std=self.pre_std
                ),
                SCORE_FUNC_DICT[CusumScoreFunction.change.value](
                    data=data, pre_mean=self.pre_mean, pre_std=self.pre_std
                ),
            )
        else:
            return PredictFunctionValues(self._zeros_ts(data), self._zeros_ts(data))

    def _zeros_ts(self, data: TimeSeriesData) -> TimeSeriesData:
        return TimeSeriesData(
            time=data.time,
            value=pd.Series(
                np.zeros(len(data)),
                name=data.value.name if data.value.name else DEFAULT_VALUE_NAME,
                copy=False,
            ),
        )

    def _check_window_sizes(self, frequency_sec: int) -> None:
        """Checks window sizes.

        Function to check if historical_window, scan_window, and step_window are suitable
        for a given TS data and historical_data.
        We have already checked if self.step_window < self.scan_window in init func when self.step_window is not None.
        """
        if self.step_window is not None:
            if self.step_window >= self.scan_window:
                raise ParameterError(
                    "Step window is supposed to be smaller than scan window to ensure we "
                    "have overlap for scan windows."
                )
            if self.step_window < frequency_sec:
                raise ParameterError(
                    "Step window is supposed to be greater than TS granularity. "
                    f"TS granularity is: {frequency_sec} seconds. "
                    "Please provide a larger step window."
                )
        # if step_window is None, step_window = min(self.scan_window/2, *** + frequency_sec)
        # in order to make sure step_window >= frequency_sec, we need to make sure
        # self.scan_window >= 2 * frequency_sec
        if (
            self.scan_window < 2 * frequency_sec
            or self.historical_window < 2 * frequency_sec
        ):
            raise ParameterError(
                "Scan window and historical window are supposed to be >= 2 * TS granularity. "
                f"TS granularity is: {frequency_sec} seconds. "
                "Please provide a larger scan window or historical_window."
            )

    def fit_predict(  # noqa:  C901
        self,
        data: TimeSeriesData,
        historical_data: Optional[TimeSeriesData] = None,
        **kwargs: Any,
    ) -> AnomalyResponse:
        """This function combines fit and predict and return anomaly socre for data.

        It requires scan_window > step_window.

        The relationship between two consective cusum runs in the loop is shown as below:

        >>> |---historical_window---|---scan_window---|
        >>>                                           |-step_window-|
        >>>               |---historical_window---|---scan_window---|

        # requirement: scan window > step window
        * scan_window: the window size in seconds to detect change point
        * historical_window: the window size in seconds to provide historical data
        * step_window: the window size in seconds to specify the step size between two scans

        Args:
            data: :class:`onclusiveml.ts.constants.TimeSeriesData` object representing the data
            historical_data: :class:`onclusiveml.ts.constants.TimeSeriesData` object representing the history.

        Returns:
            The anomaly response contains the anomaly scores.
        """
        # get parameters
        scan_window = self.scan_window
        historical_window = self.historical_window
        step_window = self.step_window
        threshold = self.threshold
        delta_std_ratio = self.delta_std_ratio
        magnitude_quantile = self.magnitude_quantile
        magnitude_ratio = self.magnitude_ratio
        change_directions = self.change_directions
        score_func = self.score_func
        remove_seasonality = self.remove_seasonality
        season_period_freq = self.season_period_freq

        scan_window = pd.Timedelta(scan_window, unit="s")
        historical_window = pd.Timedelta(historical_window, unit="s")
        # pull all the data in historical data
        if historical_data is not None:
            # make a copy of historical data
            org_hist_len = len(historical_data)
            historical_data = historical_data[:]
            historical_data.extend(data, validate=False)
        else:
            # When historical_data is not provided, will use part of data as
            # historical_data, and fill with zero anomaly score.
            historical_data = data[:]
            org_hist_len = 0

        frequency = historical_data.freq_to_timedelta()
        if frequency is None or frequency is pd.NaT:
            # Use the top frequency if any, when not able to infer from data.
            freq_counts = (
                historical_data.time.diff().value_counts().sort_values(ascending=False)
            )
            if freq_counts.iloc[0] >= int(len(historical_data)) * 0.5 - 1:
                frequency = freq_counts.index[0]
            else:
                _log.debug(f"freq_counts: {freq_counts}")
                raise IrregularGranularityException(IRREGULAR_GRANULARITY_ERROR)
        # check if historical_window, scan_window, and step_window are suitable for given TSs
        frequency_sec = frequency.total_seconds()
        self._check_window_sizes(frequency_sec)

        if remove_seasonality:
            sh_data = SeasonalityHandler(
                data=historical_data, seasonal_period=season_period_freq
            )
            historical_data = sh_data.remove_seasonality()

        smooth_window = int(scan_window.total_seconds() / frequency_sec)
        if smooth_window > 1:
            smooth_historical_value = pd.Series(
                np.convolve(
                    historical_data.value.values, np.ones(smooth_window), mode="full"
                )[: 1 - smooth_window]
                / smooth_window,
                name=historical_data.value.name,
                copy=False,
            )
            smooth_historical_data = TimeSeriesData(
                time=historical_data.time, value=smooth_historical_value
            )
        else:
            smooth_historical_data = historical_data

        anomaly_start_time = max(
            historical_data.time.iloc[0] + historical_window, data.time.iloc[0]
        )
        if anomaly_start_time > historical_data.time.iloc[-1]:
            # if len(all data) is smaller than historical window return zero score
            # Calling first _predict to poulate self.change_point_delta
            predict_results = self._predict(
                smooth_historical_data[-len(data) :], score_func
            )
            return AnomalyResponse(
                scores=predict_results.score,
                confidence_band=None,
                predicted_ts=None,
                anomaly_magnitude_ts=predict_results.absolute_change,
                stat_sig_ts=None,
            )
        anomaly_start_idx = self._time2idx(data, anomaly_start_time, "right")
        anomaly_start_time = data.time.iloc[anomaly_start_idx]
        score_tsd = self._zeros_ts(data[:anomaly_start_idx])
        change_tsd = self._zeros_ts(data[:anomaly_start_idx])

        if (
            historical_data.time.iloc[-1] - historical_data.time.iloc[0] + frequency
            < scan_window
        ):
            # if len(all data) is smaller than scan data return zero score
            # Calling first _predict to poulate self.change_point_delta
            predict_results = self._predict(
                smooth_historical_data[-len(data) :], score_func
            )
            return AnomalyResponse(
                scores=predict_results.score,
                confidence_band=None,
                predicted_ts=None,
                anomaly_magnitude_ts=predict_results.absolute_change,
                stat_sig_ts=None,
            )

        if step_window is None:
            # if step window is not provide use the time range of data or
            # half of the scan_window.
            step_window = min(
                scan_window / 2,
                (data.time.iloc[-1] - data.time.iloc[0])
                + frequency,  # to include the last data point
            )
        else:
            step_window = pd.Timedelta(step_window, unit="s")
        # if need trans to multi-TS
        # TS needs to have regular granularity, otherwise cannot transfer uni-TS to multi-TS, because
        # columns might have different length
        n_hist_win_pts = int(
            np.ceil(historical_window.total_seconds() / frequency_sec)
        )  # match _time2idx --- right

        multi_ts_len = int(
            np.ceil(
                (historical_window.total_seconds() + step_window.total_seconds())
                / frequency_sec
            )
        )  # match _time2idx --- left + 1
        n_step_win_pts = multi_ts_len - n_hist_win_pts
        multi_dim = (
            len(historical_data[anomaly_start_idx + org_hist_len :]) // n_step_win_pts
        )

        if self.vectorized:
            if (
                step_window.total_seconds() % frequency_sec == 0
                and historical_window.total_seconds() % frequency_sec
                == 0  # otherwise in the loop around row 715, each iteration might have slightly different data length
                and pd.infer_freq(historical_data.time.values)
                is not None  # regular granularity
                and multi_dim >= 2
            ):
                self.vectorized_trans_flag = True
                _log.info("Using VectorizedCUSUMDetectorModel.")
            else:
                self.vectorized_trans_flag = False
                _log.info("Cannot transfer to multi-variate TS.")

        else:
            self.vectorized_trans_flag = False
        # if need trans to multi-TS
        if self.vectorized_trans_flag:
            end_idx = anomaly_start_idx + org_hist_len + multi_dim * n_step_win_pts
            new_historical_data = self._reorganize_big_data(
                historical_data[
                    max(anomaly_start_idx - n_hist_win_pts + org_hist_len, 0) : end_idx
                ],
                multi_ts_len,
                n_step_win_pts,
            )

            new_smooth_historical_data = self._reorganize_big_data(
                smooth_historical_data[
                    max(anomaly_start_idx - n_hist_win_pts + org_hist_len, 0) : end_idx
                ],
                multi_ts_len,
                n_step_win_pts,
            )
            # remaining_part = historical_data[end_idx:]
            ss_detect = VectorizedCUSUMDetectorModel(
                scan_window=self.scan_window,
                historical_window=self.historical_window,
                step_window=step_window.total_seconds(),
                threshold=threshold,
                delta_std_ratio=delta_std_ratio,
                magnitude_quantile=magnitude_quantile,
                magnitude_ratio=magnitude_ratio,
                change_directions=change_directions,
                score_func=score_func,
                remove_seasonality=False,  # already removed
                adapted_pre_mean=False,
            )

            column_index = new_historical_data.value.columns

            ss_detect.alert_fired: pd.Series = pd.Series(False, index=column_index)

            ss_detect.pre_mean: pd.Series = pd.Series(0, index=column_index)

            ss_detect.pre_std: pd.Series = pd.Series(1, index=column_index)

            ss_detect.alert_change_direction: pd.Series = pd.Series(
                "None", index=column_index
            )

            ss_detect.number_of_normal_scan: pd.Series = pd.Series(
                0, index=column_index
            )
            ss_detect.cps = [[] for _ in range(len(column_index))]
            ss_detect.cps_meta = [[] for _ in range(len(column_index))]

            ss_detect._fit(
                data=TimeSeriesData(),
                historical_data=new_historical_data,
                scan_window=cast(Union[int, pd.Timedelta], scan_window),
                threshold=threshold,
                delta_std_ratio=delta_std_ratio,
                magnitude_quantile=magnitude_quantile,
                magnitude_ratio=magnitude_ratio,
                change_directions=change_directions,
            )

            for c in range(new_historical_data.value.shape[1]):
                in_data = TimeSeriesData(
                    time=new_historical_data.time,
                    value=new_historical_data.value.iloc[:, c],
                )

                res_cp = self._fit_vec_row(
                    vec_data_row=in_data,
                    scan_window=cast(Union[int, pd.Timedelta], scan_window),
                    changepoints=ss_detect.cps_meta[c],
                    time_adjust=pd.Timedelta(c * step_window, "s"),
                    change_directions=change_directions,
                    delta_std_ratio=delta_std_ratio,
                )
                ss_detect.pre_mean[c] = self.pre_mean
                ss_detect.pre_std[c] = self.pre_std
                ss_detect.alert_fired[c] = self.alert_fired
                ss_detect.cps[c] = res_cp

            predict_results = ss_detect._predict(
                new_smooth_historical_data[-n_step_win_pts:],
                score_func=score_func,
            )
            score_tsd_vec, change_tsd_vec = self._reorganize_back(
                predict_results.score,
                predict_results.absolute_change,
                historical_data.value.name,
            )
            score_tsd.extend(
                score_tsd_vec,
                validate=False,
            )
            change_tsd.extend(change_tsd_vec, validate=False)

        else:

            for start_time in pd.date_range(
                anomaly_start_time,
                min(
                    data.time.iloc[-1]
                    + frequency
                    - step_window,  # to include last data point
                    data.time.iloc[
                        -1
                    ],  # make sure start_time won't beyond last data time
                ),
                freq=step_window,
            ):
                _log.debug(f"start_time {start_time}")
                historical_start = self._time2idx(
                    historical_data, start_time - historical_window, "right"
                )
                _log.debug(f"historical_start {historical_start}")
                historical_end = self._time2idx(historical_data, start_time, "right")
                _log.debug(f"historical_end {historical_end}")
                scan_end = self._time2idx(
                    historical_data, start_time + step_window, "left"
                )
                _log.debug(f"scan_end {scan_end}")
                in_data = historical_data[historical_end : scan_end + 1]
                if len(in_data) == 0:
                    # skip if there is no data in the step_window
                    continue
                in_hist = historical_data[historical_start:historical_end]

                self._fit(
                    in_data,
                    in_hist,
                    scan_window=cast(Union[int, pd.Timedelta], scan_window),
                    threshold=threshold,
                    delta_std_ratio=delta_std_ratio,
                    magnitude_quantile=magnitude_quantile,
                    magnitude_ratio=magnitude_ratio,
                    change_directions=change_directions,
                )

                predict_results = self._predict(
                    smooth_historical_data[historical_end : scan_end + 1],
                    score_func=score_func,
                )
                score_tsd.extend(
                    predict_results.score,
                    validate=False,
                )
                change_tsd.extend(predict_results.absolute_change, validate=False)
        # Handle the remaining data
        remain_data_len = len(data) - len(score_tsd)
        if remain_data_len > 0:
            scan_end = len(historical_data)
            historical_end = len(historical_data) - remain_data_len
            historical_start = self._time2idx(
                historical_data,
                historical_data.time.iloc[historical_end] - historical_window,
                "left",
            )
            in_data = historical_data[historical_end:scan_end]
            in_hist = historical_data[historical_start:historical_end]
            self._fit(
                in_data,
                in_hist,
                scan_window=cast(Union[int, pd.Timedelta], scan_window),
                threshold=threshold,
                delta_std_ratio=delta_std_ratio,
                magnitude_quantile=magnitude_quantile,
                magnitude_ratio=magnitude_ratio,
                change_directions=change_directions,
            )
            predict_results = self._predict(
                smooth_historical_data[historical_end:scan_end],
                score_func=score_func,
            )
            score_tsd.extend(
                predict_results.score,
                validate=False,
            )
            change_tsd.extend(predict_results.absolute_change, validate=False)

        score_tsd.time = data.time
        change_tsd.time = data.time

        return AnomalyResponse(
            scores=score_tsd,
            confidence_band=None,
            predicted_ts=None,
            anomaly_magnitude_ts=change_tsd,
            stat_sig_ts=None,
        )

    def _reorganize_big_data(
        self,
        org_data: TimeSeriesData,
        multi_ts_len: int,
        n_step_win_pts: int,
    ) -> TimeSeriesData:
        multi_ts_time_df = org_data[:multi_ts_len].time.copy()
        multi_ts_val = [list(org_data[:multi_ts_len].value)]
        for i in range(multi_ts_len, len(org_data), n_step_win_pts):
            multi_ts_val.append(
                list(
                    org_data[
                        i - multi_ts_len + n_step_win_pts : i + n_step_win_pts
                    ].value
                )
            )

        multi_ts_val_df = pd.DataFrame(multi_ts_val).T

        multi_ts_df = pd.concat([multi_ts_time_df, multi_ts_val_df], axis=1)
        df_names = ["val_" + str(i) for i in range(multi_ts_val_df.shape[1])]
        multi_ts_df.columns = ["time"] + df_names

        return TimeSeriesData(multi_ts_df)

    def _reorganize_back(
        self,
        scores: TimeSeriesData,
        magnitude_ts: TimeSeriesData,
        name: str,
    ) -> Tuple[TimeSeriesData, TimeSeriesData]:
        anom_scores_val_array = np.asarray(scores.value)
        anom_mag_val_array = np.asarray(magnitude_ts.value)
        freq = scores.time[1] - scores.time[0]
        time_need = pd.date_range(
            start=scores.time.iloc[0],
            end=None,
            periods=anom_scores_val_array.shape[0] * anom_scores_val_array.shape[1],
            freq=freq,
        )

        anom_scores_val_1d = pd.Series(
            anom_scores_val_array.T.reshape([-1]),
            name=name,
        )

        anom_scores_ts = TimeSeriesData(time=time_need, value=anom_scores_val_1d)

        anom_mag_val_1d = pd.Series(
            anom_mag_val_array.T.reshape([-1]),
            name=name,
        )

        anom_mag_ts = TimeSeriesData(time=time_need, value=anom_mag_val_1d)

        return anom_scores_ts, anom_mag_ts

    def _time2idx(self, tsd: TimeSeriesData, time: datetime, direction: str) -> int:
        """This function get the index of the TimeSeries data given a datatime.

        left takes the index on the left of the time stamp (inclusive) right takes the index on the right of the time
        stamp (exclusive)
        """
        if direction == "right":
            return np.argwhere((tsd.time >= time).values).min()
        elif direction == "left":
            return np.argwhere((tsd.time < time).values).max()
        else:
            raise InternalError("direction can only be right or left")

    def fit(
        self,
        data: TimeSeriesData,
        historical_data: Optional[TimeSeriesData] = None,
        **kwargs: Any,
    ) -> None:
        """Fit model."""
        self.fit_predict(data, historical_data)

    def predict(
        self,
        data: TimeSeriesData,
        historical_data: Optional[TimeSeriesData] = None,
        **kwargs: Any,
    ) -> AnomalyResponse:
        """Predict is not implemented."""
        raise InternalError("predict is not implemented, call fit_predict() instead")


class VectorizedCUSUMDetectorModel(CUSUMDetectorModel):
    """VectorizedCUSUMDetectorModel detects change points for multivariate input timeseries in vectorized form.

    The logic is based on CUSUMDetectorModel, and runs VectorizedCUSUMDetector.

    VectorizedCUSUMDetectorModel runs VectorizedCUSUMDetector multiple times to
    detect multiple change points.
    In each run, CUSUMDetector will use historical_window + scan_window as
    input time series, and find change point in scan_window. The DetectorModel stores
    change points and returns anomaly score.

    Attributes:
        cps: Change points detected in unixtime.
        alert_fired: If a change point is detected and the anomaly still present.
        pre_mean: Previous baseline mean.
        pre_std: Previous baseline std.
        number_of_normal_scan: Number of scans with mean returned back to baseline.
        alert_change_direction: Increase or decrease.
        scan_window: Length in seconds of scan window.
        historical_window: Length in seconds of historical window.
        step_window: The time difference between CUSUM runs.
        threshold: CUSUMDetector threshold.
        delta_std_ratio: The mean delta have to larger than this parameter times std of
            the data to be consider as a change.
        magnitude_quantile: See in CUSUMDetector.
        magnitude_ratio: See in CUSUMDetector.
        score_func: The score function to calculate the anomaly score.
        remove_seasonality: If apply STL to remove seasonality.
        season_period_freq: str = "daily" for seasonaly decomposition.
        adapted_pre_mean: bool, whether using a rolling pre-mean and pre-std when calculating
            anomaly scores (when alert_fired = True).
    """

    def __init__(
        self,
        serialized_model: Optional[bytes] = None,
        scan_window: Optional[int] = None,
        historical_window: Optional[int] = None,
        step_window: Optional[int] = None,
        threshold: float = CUSUMDefaultArgs.threshold,
        delta_std_ratio: float = CUSUMDefaultArgs.delta_std_ratio,
        magnitude_quantile: Optional[float] = CUSUMDefaultArgs.magnitude_quantile,
        magnitude_ratio: float = CUSUMDefaultArgs.magnitude_ratio,
        change_directions: Optional[List[str]] = CUSUMDefaultArgs.change_directions,
        score_func: Union[str, CusumScoreFunction] = DEFAULT_SCORE_FUNCTION,
        remove_seasonality: bool = CUSUMDefaultArgs.remove_seasonality,
        season_period_freq: str = "daily",
        adapted_pre_mean: Optional[bool] = None,
    ) -> None:
        if serialized_model:
            previous_model = json.loads(serialized_model)
            self.cps: List[List[int]] = previous_model["cps"]
            self.cps_meta: List[List[CUSUMChangePoint]] = previous_model["cps_meta"]
            self.alert_fired: pd.Series = previous_model["alert_fired"]
            self.pre_mean: pd.Series = previous_model["pre_mean"]
            self.pre_std: pd.Series = previous_model["pre_std"]
            self.number_of_normal_scan: pd.Series = previous_model[
                "number_of_normal_scan"
            ]
            self.alert_change_direction: pd.Series = previous_model[
                "alert_change_direction"
            ]
            self.scan_window: int = previous_model["scan_window"]
            scan_window = previous_model["scan_window"]
            self.historical_window: int = previous_model["historical_window"]
            self.step_window: int = previous_model["step_window"]
            step_window = previous_model["step_window"]
            self.threshold: float = previous_model["threshold"]
            self.delta_std_ratio: float = previous_model["delta_std_ratio"]
            self.magnitude_quantile: Optional[float] = previous_model[
                "magnitude_quantile"
            ]
            self.magnitude_ratio: float = previous_model["magnitude_ratio"]
            self.change_directions: Optional[List[str]] = previous_model[
                "change_directions"
            ]
            self.score_func: CusumScoreFunction = previous_model["score_func"]
            if "remove_seasonality" in previous_model:
                self.remove_seasonality: bool = previous_model["remove_seasonality"]
            else:
                self.remove_seasonality: bool = remove_seasonality

            self.season_period_freq: str = previous_model.get(
                "season_period_freq", "daily"
            )
            # If adapted_pre_mean is provided, it should supersede existing values
            if adapted_pre_mean is not None:
                self.adapted_pre_mean: bool = adapted_pre_mean
            else:
                self.adapted_pre_mean: bool = previous_model.get(
                    "adapted_pre_mean", False
                )

        elif scan_window is not None and historical_window is not None:
            self.serialized_model: Optional[bytes] = serialized_model
            self.scan_window: int = scan_window
            self.historical_window: int = historical_window
            self.step_window: int = cast(int, step_window)
            self.threshold: float = threshold
            self.delta_std_ratio: float = delta_std_ratio
            self.magnitude_quantile: Optional[float] = magnitude_quantile
            self.magnitude_ratio: float = magnitude_ratio

            if isinstance(change_directions, str):
                self.change_directions = [change_directions]
            else:
                self.change_directions = change_directions

            self.remove_seasonality: bool = remove_seasonality
            self.season_period_freq = season_period_freq
            # We allow score_function to be a str for compatibility with param tuning
            if isinstance(score_func, str):
                if score_func in STR_TO_SCORE_FUNC:
                    score_func = STR_TO_SCORE_FUNC[score_func]
                else:
                    score_func = DEFAULT_SCORE_FUNCTION
            self.score_func: CusumScoreFunction = score_func.value
            self.adapted_pre_mean: bool = adapted_pre_mean or False

        else:
            raise ParameterError(
                "You must provide either serialized model or values for "
                "scan_window and historical_window."
            )

    def _set_alert_off_multi_ts(self, set_off_mask: pd.Series) -> None:
        self.alert_fired &= ~set_off_mask
        self.number_of_normal_scan[set_off_mask] = 0

    def _set_alert_on_multi_ts(
        self,
        set_on_mask: pd.Series,
        baseline_mean: pd.Series,
        baseline_std: pd.Series,
        alert_change_direction: pd.Series,
    ) -> None:
        self.alert_change_direction[set_on_mask] = alert_change_direction
        self.pre_mean[set_on_mask] = baseline_mean.combine_first(self.pre_mean)
        self.pre_std[set_on_mask] = baseline_std.combine_first(self.pre_std)

    def _if_back_to_normal(
        self,
        cur_mean: pd.Series,
        change_directions: Optional[List[str]],
        delta_std_ratio: float = CUSUMDefaultArgs.delta_std_ratio,
    ) -> pd.Series:
        if change_directions is not None:
            increase, decrease = (
                "increase" in change_directions,
                "decrease" in change_directions,
            )
        else:
            increase, decrease = True, True
        check_increase = np.array([])
        check_decrease = np.array([])
        for x in self.alert_change_direction:
            cur_increase = cur_decrease = 0
            if x == "increase":
                cur_increase = 0 if increase else np.inf
                cur_decrease = delta_std_ratio if decrease else np.inf
            elif x == "decrease":
                cur_increase = delta_std_ratio if increase else np.inf
                cur_decrease = 0 if decrease else np.inf
            check_increase = np.append(check_increase, cur_increase)
            check_decrease = np.append(check_decrease, cur_decrease)
        return (self.pre_mean - check_decrease * self.pre_std <= cur_mean) * (
            cur_mean <= self.pre_mean + check_increase * self.pre_std
        )

    def _fit(
        self,
        data: TimeSeriesData,
        historical_data: TimeSeriesData,
        scan_window: Union[int, pd.Timedelta],
        threshold: float = CUSUMDefaultArgs.threshold,
        delta_std_ratio: float = CUSUMDefaultArgs.delta_std_ratio,
        magnitude_quantile: Optional[float] = CUSUMDefaultArgs.magnitude_quantile,
        magnitude_ratio: float = CUSUMDefaultArgs.magnitude_ratio,
        change_directions: Optional[List[str]] = CUSUMDefaultArgs.change_directions,
    ) -> None:
        """Fit CUSUM model.

        Args:
            data: the new data the model never seen
            historical_data: the historical data, `historical_data` have to end with the
                datapoint right before the first data point in `data`
            scan_window: scan window length in seconds, scan window is the window where
                cusum search for changepoint(s)
            threshold: changepoint significant level, higher the value more changepoints
                detected
            delta_std_ratio: the mean change have to larger than `delta_std_ratio` *
            `std(data[:changepoint])` to be consider as a change, higher the value
            less changepoints detected
            magnitude_quantile: float, the quantile for magnitude comparison, if
                none, will skip the magnitude comparison;
            magnitude_ratio: float, comparable ratio;
            change_directions: a list contain either or both 'increase' and 'decrease' to
                specify what type of change to detect;
        """
        if len(data) > 0:
            historical_data.extend(data, validate=False)
        n = len(historical_data)
        scan_start_time = historical_data.time.iloc[-1] - pd.Timedelta(
            scan_window, unit="s"
        )
        scan_start_index = max(
            0, np.argwhere((historical_data.time >= scan_start_time).values).min()
        )

        n_pts = historical_data.value.shape[0]
        # separate into two cases: alert off and alert on
        # if scan window is less than 2 data poins and there is no alert fired
        # skip this scan
        alert_set_on_mask = (~self.alert_fired[:]) & (n - scan_start_index > 1)
        alert_set_off_mask = self.alert_fired.copy()
        # [Case 1] if alert is off (alert_fired[i] is False)
        if alert_set_on_mask.any():
            # Use VectorizedCUSUMDetector
            detector = VectorizedCUSUMDetector(historical_data)
            changepoints = detector.detector(
                interest_window=[scan_start_index, n],
                threshold=threshold,
                delta_std_ratio=delta_std_ratio,
                magnitude_quantile=magnitude_quantile,
                magnitude_ratio=magnitude_ratio,
                change_directions=change_directions,
            )

            cps = [
                (
                    sorted(x, key=lambda x: x.start_time)[0]
                    if x and alert_set_on_mask[i]
                    else None
                )
                for i, x in enumerate(changepoints)
            ]

            alert_set_on_mask &= np.array([x is not None for x in cps])
            # mask1 is used to calculate avg and std with different changepoint index
            mask1 = np.tile(alert_set_on_mask, (n_pts, 1))
            for i, cp in enumerate(cps):
                if cp is not None:
                    mask1[(cp.cp_index + 1) :, i] = False
                    self.cps[i].append(int(cp.start_time.value / 1e9))
                    self.cps_meta[i].append(cp)
                    if len(self.cps[i]) > MAX_CHANGEPOINT:
                        self.cps[i].pop(0)
                        self.cps_meta[i].pop(0)

            avg = np.divide(
                np.sum(np.multiply(historical_data.value, mask1), axis=0),
                np.sum(mask1, axis=0),
            )
            std = np.sqrt(
                np.divide(
                    np.sum(
                        np.multiply(np.square(historical_data.value - avg), mask1),
                        axis=0,
                    ),
                    np.sum(mask1, axis=0),
                )
            )
            self._set_alert_on_multi_ts(
                alert_set_on_mask,
                avg,
                std,
                [x.direction if x else None for x in cps],
            )
            self.alert_fired |= np.array([x is not None for x in cps])
        # [Case 2] if alert is on (alert_fired[i] is True)
        # set off alert when:
        # [2.1] the mean of current dataset is back to normal and num_normal_scan >= NORMAL_TOLERENCE
        # [2.2] alert retention > CHANGEPOINT_RETENTION
        if alert_set_off_mask.any():
            mask2 = np.tile(alert_set_off_mask, (n_pts, 1))
            mask2[:scan_start_index, :] = False
            cur_mean = np.divide(
                np.sum(np.multiply(historical_data.value, mask2), axis=0),
                np.sum(mask2, axis=0),
            )
            if self.adapted_pre_mean:
                mask3 = np.tile(alert_set_off_mask, (n_pts, 1))
                mask3[scan_start_index:, :] = False
                pre_mean = np.divide(
                    np.sum(np.multiply(historical_data.value, mask3), axis=0),
                    np.sum(mask3, axis=0),
                )

                pre_std = np.sqrt(
                    np.divide(
                        np.sum(
                            np.multiply(
                                np.square(historical_data.value - pre_mean), mask3
                            ),
                            axis=0,
                        ),
                        np.sum(mask3, axis=0),
                    )
                )

                self.pre_mean[alert_set_off_mask] = pre_mean.combine_first(
                    self.pre_mean
                )
                self.pre_std[alert_set_off_mask] = pre_std.combine_first(self.pre_std)

            is_normal = self._if_back_to_normal(
                cur_mean, change_directions, delta_std_ratio
            )
            # if current mean is normal, num_normal_scan increment 1, if not, num_normal_scan set to 0
            self.number_of_normal_scan += is_normal
            # set off alert
            # [case 2.1]
            tmp1 = self.number_of_normal_scan >= NORMAL_TOLERENCE
            self._set_alert_off_multi_ts(alert_set_off_mask & tmp1 & is_normal)
            self.number_of_normal_scan[~is_normal] = 0
            # [case 2.2]
            current_time = int(data.time.max().value / 1e9)
            tmp2 = np.asarray(
                [
                    current_time - x[-1] > CHANGEPOINT_RETENTION if len(x) else False
                    for x in self.cps
                ]
            )
            self._set_alert_off_multi_ts(alert_set_off_mask & tmp2)

    def _predict(
        self,
        data: TimeSeriesData,
        score_func: CusumScoreFunction = CusumScoreFunction.change,
    ) -> PredictFunctionValues:
        """Performs anomaly detection."""
        cp = [x[-1] if len(x) else None for x in self.cps]
        tz = data.tz()
        if tz is None:
            change_time = [pd.to_datetime(x, unit="s") if x else None for x in cp]
        else:
            change_time = [
                pd.to_datetime(x, unit="s", utc=True).tz_convert(tz) if x else None
                for x in cp
            ]
        n_pts = data.value.shape[0]
        first_ts = data.time.iloc[0]
        cp_index = [
            data.time.index[data.time == x][0] if x and x >= first_ts else None
            for x in change_time
        ]
        ret = PredictFunctionValues(
            SCORE_FUNC_DICT[score_func](
                data=data, pre_mean=self.pre_mean, pre_std=self.pre_std
            ),
            SCORE_FUNC_DICT[CusumScoreFunction.change.value](
                data=data, pre_mean=self.pre_mean, pre_std=self.pre_std
            ),
        )
        # in the following 2 cases, fill score with 0 by mask 0:
        # (i) if no alert fired for a timeseries (change_time is None)
        # (ii) if alert fired, fill 0 for time index before cp_index
        set_zero_mask = np.tile(~self.alert_fired, (n_pts, 1))
        for i, c in enumerate(cp_index):
            if c is not None:
                set_zero_mask[: (c + 1), i] = True
        ret.score.value[set_zero_mask] = 0
        ret.absolute_change.value[set_zero_mask] = 0
        return ret

    def _zeros_ts(self, data: TimeSeriesData) -> TimeSeriesData:
        """Zero time series."""
        if len(data) > 0:
            return TimeSeriesData(
                time=data.time,
                value=pd.DataFrame(
                    np.zeros(data.value.shape), columns=data.value.columns
                ),
            )
        else:
            return TimeSeriesData()

    def run_univariate_cusumdetectormodel(
        self, data: TimeSeriesData, historical_data: TimeSeriesData
    ) -> AnomalyResponse:
        """Run univariate cusum detector model."""
        d = CUSUMDetectorModel(
            serialized_model=self.serialized_model,
            scan_window=self.scan_window,
            historical_window=self.historical_window,
            step_window=self.step_window,
            threshold=self.threshold,
            delta_std_ratio=self.delta_std_ratio,
            magnitude_quantile=self.magnitude_quantile,
            magnitude_ratio=self.magnitude_ratio,
            change_directions=self.change_directions,
            score_func=self.score_func,
            remove_seasonality=self.remove_seasonality,
        )
        return d.fit_predict(data, historical_data)

    def fit_predict(
        self,
        data: TimeSeriesData,
        historical_data: Optional[TimeSeriesData] = None,
        **kwargs: Any,
    ) -> AnomalyResponse:
        """This function combines fit and predict and return anomaly socre for data.

        It requires scan_window > step_window.
        The relationship between two consective cusum runs in the loop is shown as below:

        >>> |---historical_window---|---scan_window---|
        >>>                                           |-step_window-|
        >>>               |---historical_window---|---scan_window---|

        # requirement: scan window > step window
        * scan_window: the window size in seconds to detect change point
        * historical_window: the window size in seconds to provide historical data
        * step_window: the window size in seconds to specify the step size between two scans

        Args:
            data: :class:`onclusiveml.ts.constants.TimeSeriesData` object representing the data
            historical_data: :class:`onclusiveml.ts.constants.TimeSeriesData` object representing the history.

        Returns:
            The anomaly response contains the anomaly scores.
        """
        # init parameters after getting input data
        num_timeseries = (
            data.value.shape[1] if isinstance(data.value, pd.DataFrame) else 1
        )
        if num_timeseries == 1:
            _log.info(
                "Input timeseries is univariate. CUSUMDetectorModel is preferred."
            )
            assert historical_data is not None
            return self.run_univariate_cusumdetectormodel(data, historical_data)

        self.alert_fired: pd.Series = pd.Series(False, index=data.value.columns)
        self.pre_mean: pd.Series = pd.Series(0, index=data.value.columns)
        self.pre_std: pd.Series = pd.Series(1, index=data.value.columns)
        self.alert_change_direction: pd.Series = pd.Series(
            "None", index=data.value.columns
        )
        self.number_of_normal_scan: pd.Series = pd.Series(0, index=data.value.columns)
        self.cps = [[] for _ in range(num_timeseries)]
        self.cps_meta = [[] for _ in range(num_timeseries)]
        # get parameters
        scan_window = self.scan_window
        historical_window = self.historical_window
        step_window = self.step_window
        threshold = self.threshold
        delta_std_ratio = self.delta_std_ratio
        magnitude_quantile = self.magnitude_quantile
        magnitude_ratio = self.magnitude_ratio
        change_directions = self.change_directions
        score_func = self.score_func
        remove_seasonality = self.remove_seasonality
        season_period_freq = self.season_period_freq

        scan_window = pd.Timedelta(scan_window, unit="s")
        historical_window = pd.Timedelta(historical_window, unit="s")
        # pull all the data in historical data
        if historical_data is not None:
            # make a copy of historical data
            historical_data = historical_data[:]
            historical_data.extend(data, validate=False)
        else:
            # When historical_data is not provided, will use part of data as
            # historical_data, and fill with zero anomaly score.
            historical_data = data[:]

        frequency = historical_data.freq_to_timedelta()
        if frequency is None or frequency is pd.NaT:
            # Use the top frequency if any, when not able to infer from data.
            freq_counts = (
                historical_data.time.diff().value_counts().sort_values(ascending=False)
            )
            if freq_counts.iloc[0] >= int(len(historical_data)) * 0.5 - 1:
                frequency = freq_counts.index[0]
            else:
                _log.debug(f"freq_counts: {freq_counts}")
                raise IrregularGranularityException(IRREGULAR_GRANULARITY_ERROR)
        # check if historical_window, scan_window, and step_window are suitable for given TSs
        self._check_window_sizes(frequency.total_seconds())

        if remove_seasonality:
            sh_data = SeasonalityHandler(
                data=historical_data, seasonal_period=season_period_freq
            )
            historical_data = sh_data.remove_seasonality()

        smooth_window = int(scan_window.total_seconds() / frequency.total_seconds())
        if smooth_window > 1:
            smooth_historical_value = (
                historical_data.value.apply(
                    lambda x: np.convolve(x, np.ones(smooth_window), mode="full"),
                    axis=0,
                )[: 1 - smooth_window]
                / smooth_window
            )
            smooth_historical_value = cast(pd.DataFrame, smooth_historical_value)
            smooth_historical_data = TimeSeriesData(
                time=historical_data.time, value=smooth_historical_value
            )
        else:
            smooth_historical_data = historical_data

        anomaly_start_time = max(
            historical_data.time.iloc[0] + historical_window, data.time.iloc[0]
        )
        if anomaly_start_time > historical_data.time.iloc[-1]:
            # if len(all data) is smaller than historical window return zero score
            # Calling first _predict to poulate self.change_point_delta
            predict_results = self._predict(
                smooth_historical_data[-len(data) :], score_func
            )
            return AnomalyResponse(
                scores=predict_results.score,
                confidence_band=None,
                predicted_ts=None,
                anomaly_magnitude_ts=predict_results.absolute_change,
                stat_sig_ts=None,
            )
        anomaly_start_idx = self._time2idx(data, anomaly_start_time, "right")
        anomaly_start_time = data.time.iloc[anomaly_start_idx]
        score_tsd = self._zeros_ts(data[:anomaly_start_idx])
        change_tsd = self._zeros_ts(data[:anomaly_start_idx])

        if (
            historical_data.time.iloc[-1] - historical_data.time.iloc[0] + frequency
            < scan_window
        ):
            # if len(all data) is smaller than scan data return zero score
            # Calling first _predict to poulate self.change_point_delta
            predict_results = self._predict(
                smooth_historical_data[-len(data) :], score_func
            )
            return AnomalyResponse(
                scores=predict_results.score,
                confidence_band=None,
                predicted_ts=None,
                anomaly_magnitude_ts=predict_results.absolute_change,
                stat_sig_ts=None,
            )

        if step_window is None:
            # if step window is not provide use the time range of data or
            # half of the scan_window.
            step_window = min(
                scan_window / 2,
                (data.time.iloc[-1] - data.time.iloc[0])
                + frequency,  # to include the last data point
            )
        else:
            step_window = pd.Timedelta(step_window, unit="s")
        # rolling window
        for start_time in pd.date_range(
            anomaly_start_time,
            min(
                data.time.iloc[-1]
                + frequency
                - step_window,  # to include last data point
                data.time.iloc[-1],  # make sure start_time won't beyond last data time
            ),
            freq=step_window,
        ):
            _log.debug(f"start_time {start_time}")
            historical_start = self._time2idx(
                historical_data, start_time - historical_window, "right"
            )
            _log.debug(f"historical_start {historical_start}")
            historical_end = self._time2idx(historical_data, start_time, "right")
            _log.debug(f"historical_end {historical_end}")
            scan_end = self._time2idx(historical_data, start_time + step_window, "left")
            _log.debug(f"scan_end {scan_end}")
            in_data = historical_data[historical_end : scan_end + 1]
            if len(in_data) == 0:
                # skip if there is no data in the step_window
                continue
            in_hist = historical_data[historical_start:historical_end]
            self._fit(
                in_data,
                in_hist,
                scan_window=cast(Union[int, pd.Timedelta], scan_window),
                threshold=threshold,
                delta_std_ratio=delta_std_ratio,
                magnitude_quantile=magnitude_quantile,
                magnitude_ratio=magnitude_ratio,
                change_directions=change_directions,
            )
            predict_results = self._predict(
                smooth_historical_data[historical_end : scan_end + 1],
                score_func=score_func,
            )
            score_tsd.extend(
                predict_results.score,
                validate=False,
            )
            change_tsd.extend(predict_results.absolute_change, validate=False)
        # Handle the remaining data
        remain_data_len = len(data) - len(score_tsd)
        if remain_data_len > 0:
            scan_end = len(historical_data)
            historical_end = len(historical_data) - remain_data_len
            historical_start = self._time2idx(
                historical_data,
                historical_data.time.iloc[historical_end] - historical_window,
                "left",
            )
            in_data = historical_data[historical_end:scan_end]
            in_hist = historical_data[historical_start:historical_end]
            self._fit(
                in_data,
                in_hist,
                scan_window=cast(Union[int, pd.Timedelta], scan_window),
                threshold=threshold,
                delta_std_ratio=delta_std_ratio,
                magnitude_quantile=magnitude_quantile,
                magnitude_ratio=magnitude_ratio,
                change_directions=change_directions,
            )
            predict_results = self._predict(
                smooth_historical_data[historical_end:scan_end],
                score_func=score_func,
            )
            score_tsd.extend(
                predict_results.score,
                validate=False,
            )
            change_tsd.extend(predict_results.absolute_change, validate=False)

        return AnomalyResponse(
            scores=score_tsd,
            confidence_band=None,
            predicted_ts=None,
            anomaly_magnitude_ts=change_tsd,
            stat_sig_ts=None,
        )
