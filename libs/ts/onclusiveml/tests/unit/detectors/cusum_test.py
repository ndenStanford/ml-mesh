# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""Cusum test."""

# Standard Library
from operator import attrgetter
from typing import Callable, List, Optional
from unittest import TestCase

# 3rd party libraries
import numpy as np
import pandas as pd
from parameterized.parameterized import parameterized
from scipy.stats import chi2  # @manual
from sklearn.datasets import make_spd_matrix

# Internal libraries
from onclusiveml.ts.constants import IRREGULAR_GRANULARITY_ERROR
from onclusiveml.ts.detectors.cusum import (
    CUSUMChangePoint,
    CUSUMDetector,
    CUSUMDetectorModel,
    CusumScoreFunction,
    MultiCUSUMDetector,
    VectorizedCUSUMDetector,
    VectorizedCUSUMDetectorModel,
)
from onclusiveml.ts.exceptions import (
    DataIrregularGranularityError,
    InternalError,
    ParameterError,
)
from onclusiveml.ts.timeseries import TimeSeriesData


class TestIncreaseCUSUMDetectorModel(TestCase):
    def setUp(self) -> None:
        np.random.seed(100)
        self.scan_window = 24 * 60 * 60  # in seconds
        self.historical_window = 3 * 24 * 60 * 60  # in seconds
        self.test_data_window = 16  # in hours
        self.regression_sum_score = 12  #
        df_increase = pd.DataFrame(
            {
                "ts_value": np.concatenate(
                    [np.random.normal(1, 0.2, 156), np.random.normal(1.5, 0.2, 12)]
                ),
                "time": pd.date_range("2020-01-01", periods=168, freq="H"),
            }
        )
        self.tsd = TimeSeriesData(df_increase)
        self.tsd_value_name = self.tsd.value.name
        data = self.tsd[-self.test_data_window :]

        self.model = CUSUMDetectorModel(
            scan_window=self.scan_window, historical_window=self.historical_window
        )

        self.score_tsd = self.model.fit_predict(
            data=data, historical_data=self.tsd[: -self.test_data_window]
        ).scores

        self.score_tsd_percentage_change = self.model._predict(
            data=data,
            score_func=CusumScoreFunction.percentage_change.value,
        ).score

        self.score_tsd_z_score = self.model._predict(
            data=data, score_func=CusumScoreFunction.z_score.value
        ).score

        self.serialized_model = self.model.serialize()

    @parameterized.expand(
        [
            ("increase_length_match", len, "score_tsd", "test_data_window"),
            (
                # make sure the time series name are the same
                "increase_time_series_name_match",
                lambda x: x.value.name,
                "score_tsd",
                "tsd_value_name",
            ),
            (
                # the regression is detected
                "increase_regression_detected",
                lambda x: (x.value > 0).sum(),
                "score_tsd",
                "regression_sum_score",
            ),
            (
                "increase_percentage_change_length_match",
                len,
                "score_tsd_percentage_change",
                "test_data_window",
            ),
            (
                # the regression is detected
                "increase_percentage_change_regression_detected",
                lambda x: (x.value > 0).sum(),
                "score_tsd_percentage_change",
                "regression_sum_score",
            ),
            (
                "increase_z_score_length_match",
                len,
                "score_tsd_z_score",
                "test_data_window",
            ),
            (
                # the regression is detected
                "increase_z_score_regression_detected",
                lambda x: (x.value > 0).sum(),
                "score_tsd_z_score",
                "regression_sum_score",
            ),
        ]
    )
    def test_score_tsd(
        self,
        name: str,
        func_: Callable[[TimeSeriesData], float],
        attr1: str,
        attr2: str,
    ) -> None:
        self.assertEqual(func_(attrgetter(attr1)(self)), attrgetter(attr2)(self))

    def test_serialized_model(self) -> None:
        self.assertIsInstance(self.serialized_model, bytes)

    def test_new_model(self) -> None:
        model_new = CUSUMDetectorModel(self.serialized_model)
        self.assertEqual(model_new, self.model)

    def test_model(self) -> None:
        self.assertNotEqual(
            self.model,
            CUSUMDetectorModel(
                scan_window=self.scan_window, historical_window=self.historical_window
            ),
        )


class TestDecreaseCUSUMDetectorModel(TestCase):
    def setUp(self) -> None:
        np.random.seed(100)
        scan_window = 24 * 60 * 60  # in seconds
        historical_window = 3 * 24 * 60 * 60  # in seconds
        self.test_data_window = 6  # in hours
        df_decrease = pd.DataFrame(
            {
                "ts_value": np.concatenate(
                    [np.random.normal(2, 0.2, 156), np.random.normal(1, 0.2, 12)]
                ),
                "time": pd.date_range("2020-01-01", periods=168, freq="H"),
            }
        )
        tsd = TimeSeriesData(df_decrease)
        data = tsd[-self.test_data_window :]

        model = CUSUMDetectorModel(
            scan_window=scan_window, historical_window=historical_window
        )

        _ = model.fit_predict(
            data=data, historical_data=tsd[: -self.test_data_window]
        ).scores

        self.score_tsd = model._predict(
            data=data, score_func=CusumScoreFunction.change.value
        ).score

        self.score_tsd_percentage_change = model._predict(
            data=data,
            score_func=CusumScoreFunction.percentage_change.value,
        ).score

        self.score_tsd_z_score = model._predict(
            data=data, score_func=CusumScoreFunction.z_score.value
        ).score

    @parameterized.expand(
        [
            ("decrease_length_match", len, "score_tsd"),
            (
                # the regression is detected
                "decrease_regression_detected",
                lambda x: (x.value < 0).sum(),
                "score_tsd",
            ),
            (
                "decrease_percentage_change_length_match",
                len,
                "score_tsd_percentage_change",
            ),
            (
                # the regression is detected
                "decrease_percentage_change_regression_detected",
                lambda x: (x.value < 0).sum(),
                "score_tsd_percentage_change",
            ),
            (
                "decrease_z_score_length_match",
                len,
                "score_tsd_z_score",
            ),
            (
                # the regression is detected
                "decrease_z_score_regression_detected",
                lambda x: (x.value < 0).sum(),
                "score_tsd_z_score",
            ),
        ]
    )
    def test_score_tsd(
        self, name: str, func_: Callable[[TimeSeriesData], float], attr: str
    ) -> None:
        self.assertEqual(func_(attrgetter(attr)(self)), self.test_data_window)


class TestAdhocCUSUMDetectorModel(TestCase):
    def setUp(self) -> None:
        np.random.seed(100)
        self.historical_window = 48 * 60 * 60  # in seconds
        self.scan_window = 11 * 60 * 60 + 50  # in seconds
        n = 168
        self.const_0 = 0
        self.const_12 = 12
        self.const_24 = 24
        df_increase = pd.DataFrame(
            {
                "ts_value": np.concatenate(
                    [
                        np.random.normal(1, 0.2, 48),
                        np.random.normal(0.2, 0.1, 12),
                        np.random.normal(1, 0.2, 60),
                        np.random.normal(2, 0.2, 24),
                        np.random.normal(0.9, 0.2, 24),
                    ]
                ),
                "time": pd.date_range("2020-01-01", periods=n, freq="H"),
            }
        )
        self.tsd = TimeSeriesData(df_increase)

        model = CUSUMDetectorModel(
            scan_window=self.scan_window, historical_window=self.historical_window
        )
        self.score_tsd = model.fit_predict(data=self.tsd).scores
        # test not enough data
        model = CUSUMDetectorModel(
            scan_window=self.scan_window, historical_window=self.historical_window
        )
        self.score_tsd_not_enough_data = model.fit_predict(
            data=self.tsd[-4:], historical_data=self.tsd[-8:-4]
        ).scores

        model = CUSUMDetectorModel(
            scan_window=self.scan_window, historical_window=2 * 3600
        )
        self.score_tsd_fixed_historical_window = model.fit_predict(
            data=self.tsd[-8:]
        ).scores

    @parameterized.expand(
        [
            ("adhoc", len, "score_tsd", len, "tsd"),
            (
                # the regression is went away
                "adhoc_regression_went_away",
                lambda x: x.value[-6:].sum(),
                "score_tsd",
                lambda x: x,
                "const_0",
            ),
            (
                # the increase regression is detected
                "adhoc_regression_increased",
                lambda x: (x.value > 0.5).sum(),
                "score_tsd",
                lambda x: x,
                "const_24",
            ),
            (
                # the decrease regression is detected
                "adhoc_regression_decreased",
                lambda x: (x.value < -0.45).sum(),
                "score_tsd",
                lambda x: x,
                "const_12",
            ),
            (
                # test not enough data
                "adhoc_not_enough_data_length_match",
                len,
                "score_tsd_not_enough_data",
                lambda x: len(x[-4:]),
                "tsd",
            ),
            (
                # test not enough data
                "adhoc_not_enough_data_zero_sum_score",
                lambda x: x.value.sum(),
                "score_tsd_not_enough_data",
                lambda x: x,
                "const_0",
            ),
            (
                "adhoc_length_match",
                len,
                "score_tsd_fixed_historical_window",
                lambda x: len(x[-8:]),
                "tsd",
            ),
            (
                "adhoc_zero_sum_score",
                lambda x: x.value.sum(),
                "score_tsd_fixed_historical_window",
                lambda x: x,
                "const_0",
            ),
        ]
    )
    def test_score_tsd(
        self,
        name: str,
        func_1: Callable[[TimeSeriesData], float],
        attr1: str,
        func_2: Callable[[TimeSeriesData], float],
        attr2: str,
    ) -> None:
        self.assertEqual(
            func_1(attrgetter(attr1)(self)), func_2(attrgetter(attr2)(self))
        )


class TestMissingDataCUSUMDetectorModel(TestCase):
    def setUp(self) -> None:
        df = pd.DataFrame(
            {
                "ts_value": [0] * 8,
                "time": [
                    "2020-01-01",
                    "2020-01-02",
                    "2020-01-03",
                    "2020-01-04",
                    "2020-01-05",
                    "2020-01-06",
                    "2020-01-08",
                    "2020-01-09",
                ],
            }
        )
        self.tsd = TimeSeriesData(df)
        # We also assume a bad input here
        model = CUSUMDetectorModel(
            scan_window=2 * 24 * 3600,
            historical_window=2 * 24 * 3600,
        )
        self.score_tsd = model.fit_predict(
            data=self.tsd,
        ).scores

    def test_missing_data_length_match(self) -> None:
        self.assertEqual(len(self.score_tsd), len(self.tsd))

    def test_missing_data_value_match(self) -> None:
        self.assertTrue((self.score_tsd.time.values == self.tsd.time.values).all())


class TestStreamingCUSUMDetectorModel(TestCase):
    def setUp(self) -> None:
        np.random.seed(100)
        historical_window = 48 * 60 * 60  # in seconds
        scan_window = 12 * 60 * 60  # in seconds
        self.n = 72
        df_increase = pd.DataFrame(
            {
                "ts_value": np.concatenate(
                    [np.random.normal(1, 0.2, 60), np.random.normal(1.5, 0.2, 12)]
                ),
                "time": pd.date_range("2020-01-01", periods=self.n, freq="H"),
            }
        )
        tsd = TimeSeriesData(df_increase)
        # Priming the model
        model = CUSUMDetectorModel(
            historical_window=historical_window, scan_window=scan_window
        )
        model.fit(data=tsd[:48])
        pre_serialized_model = model.serialize()

        self.anomaly_score = TimeSeriesData(
            time=pd.Series(), value=pd.Series([], name="ts_value")
        )
        # feeding 1 new data point a time
        for i in range(48, self.n):
            model = CUSUMDetectorModel(
                serialized_model=pre_serialized_model,
                historical_window=historical_window,
                scan_window=scan_window,
            )
            self.anomaly_score.extend(
                model.fit_predict(
                    data=tsd[i : i + 1], historical_data=tsd[i - 48 : i]
                ).scores,
                validate=False,
            )
            pre_serialized_model = model.serialize()
        self.anomaly_score.validate_data(
            validate_frequency=True, validate_dimension=False
        )

    def test_streaming_length_match(self) -> None:
        """Test streaming length match."""
        self.assertEqual(len(self.anomaly_score), self.n - 48)

    def test_streaming_value_match(self) -> None:
        """Test streaming value match."""
        self.assertTrue(8 <= (self.anomaly_score.value > 0).sum() <= 12)


class TestTZAwareDataCUSUMDetectorModel(TestCase):
    def setUp(self) -> None:
        np.random.seed(100)
        freq = 86400
        self.historical_window = 48 * freq  # in seconds
        self.scan_window = 12 * freq  # in seconds
        self.n = 72
        values = np.concatenate(
            [np.random.normal(1, 0.2, 60), np.random.normal(1.5, 0.2, 12)]
        )
        start_time = pd.Timestamp("2020-01-01").value // 10**9
        df = pd.DataFrame(
            {
                "ts_value": values,
                "time": np.arange(start_time, start_time + self.n * freq, freq),
            }
        )
        df_irregular = pd.DataFrame(
            {
                "ts_value": values,
                "time": np.concatenate(
                    [
                        np.arange(start_time, start_time + 24 * freq, freq),
                        np.arange(
                            start_time + 36 * freq,
                            start_time + (self.n + 12) * freq,
                            freq,
                        ),
                    ]
                ),
            }
        )
        self.tsd = TimeSeriesData(
            df, use_unix_time=True, unix_time_units="s", tz="US/Pacific"
        )
        self.tsd_irregular = TimeSeriesData(
            df_irregular, use_unix_time=True, unix_time_units="s", tz="US/Pacific"
        )

    def test_tzaware_data(self) -> None:
        # Priming the model
        model = CUSUMDetectorModel(
            historical_window=self.historical_window, scan_window=self.scan_window
        )
        model.fit(data=self.tsd[:48])
        pre_serialized_model = model.serialize()

        anomaly_score = TimeSeriesData(
            time=pd.Series(), value=pd.Series([], name="ts_value")
        )
        # feeding 1 new data point a time
        for i in range(48, self.n):
            model = CUSUMDetectorModel(
                serialized_model=pre_serialized_model,
                historical_window=self.historical_window,
                scan_window=self.scan_window,
            )
            anomaly_score.extend(
                model.fit_predict(
                    data=self.tsd[i : i + 1], historical_data=self.tsd[i - 48 : i]
                ).scores,
                validate=False,
            )
            pre_serialized_model = model.serialize()

        self.assertEqual(len(anomaly_score), self.n - 48)
        self.assertTrue(7 <= (anomaly_score.value > 0).sum() <= 12)
        self.assertTrue((anomaly_score.time.values == self.tsd[48:].time.values).all())

    def test_irregular_tzaware_data(self) -> None:
        # Priming the model
        model = CUSUMDetectorModel(
            historical_window=self.historical_window, scan_window=self.scan_window
        )
        model.fit(data=self.tsd_irregular[:48])
        pre_serialized_model = model.serialize()

        anomaly_score = TimeSeriesData(
            time=pd.Series(), value=pd.Series([], name="ts_value")
        )
        # feeding 1 new data point a time
        for i in range(48, self.n):
            model = CUSUMDetectorModel(
                serialized_model=pre_serialized_model,
                historical_window=self.historical_window,
                scan_window=self.scan_window,
            )
            anomaly_score.extend(
                model.fit_predict(
                    data=self.tsd_irregular[i : i + 1],
                    historical_data=self.tsd_irregular[i - 48 : i],
                ).scores,
                validate=False,
            )
            pre_serialized_model = model.serialize()

        self.assertEqual(len(anomaly_score), self.n - 48)
        self.assertTrue(7 <= (anomaly_score.value > 0).sum() <= 12)
        self.assertTrue(
            (anomaly_score.time.values == self.tsd_irregular[48:].time.values).all()
        )


class TestDecomposingSeasonalityCUSUMDetectorModel(TestCase):
    def setUp(self) -> None:
        np.random.seed(100)
        historical_window = 10 * 24 * 60 * 60  # in seconds
        scan_window = 12 * 60 * 60  # in seconds
        n = 480
        periodicity = 24
        self.const_0 = 0
        self.const_10 = 10

        df_sin = pd.DataFrame(
            {
                "time": pd.date_range("2020-01-01", periods=n, freq="H"),
                "ts_value": np.concatenate([20 * np.ones(n // 2), 21 * np.ones(n // 2)])
                + 4 * np.sin(2 * np.pi / periodicity * np.arange(0, n)),
            }
        )
        # removing a few data points to test the missing value handling as well
        self.tsd = TimeSeriesData(pd.concat([df_sin[:100], df_sin[103:]]))

        model = CUSUMDetectorModel(
            scan_window=scan_window,
            historical_window=historical_window,
            remove_seasonality=True,
            score_func=CusumScoreFunction.percentage_change,
        )
        self.score_tsd = model.fit_predict(
            data=self.tsd,
        ).scores

    @parameterized.expand(
        [
            (
                "decomposing_seasonality_length_match",
                len,
                "score_tsd",
                len,
                "tsd",
                lambda x, y: x == y,
            ),
            (
                # the scores set to zero after about 7 days
                "decomposing_seasonality_score_after_seven_days",
                lambda x: x.value[-72:].sum(),
                "score_tsd",
                lambda x: x,
                "const_0",
                lambda x, y: x == y,
            ),
            (
                # the increase regression is detected and is on for about 7 days
                # statsmodels version difference will result in different STL results
                "decomposing_seasonality_regression_detected",
                lambda x: np.abs((x.value > 0.01).sum() - 168),
                "score_tsd",
                lambda x: x,
                "const_10",
                lambda x, y: x < y,
            ),
            (
                # make sure the time series time are the same
                "decomposing_seasonality_time_series_same",
                lambda x: x.time.values,
                "score_tsd",
                lambda x: x.time.values,
                "tsd",
                lambda x, y: (x == y).all(),
            ),
            (
                # make sure the time series name are the same
                "decomposing_seasonality_time_series_name_check",
                lambda x: x.value.name,
                "score_tsd",
                lambda x: x.value.name,
                "tsd",
                lambda x, y: x == y,
            ),
        ]
    )
    def test_score_tsd(
        self,
        name: str,
        func_1: Callable[[TimeSeriesData], float],
        attr1: str,
        func_2: Callable[[TimeSeriesData], float],
        attr2: str,
        func_sup: Callable[[float, float], bool],
    ) -> None:
        self.assertTrue(
            func_sup(func_1(attrgetter(attr1)(self)), func_2(attrgetter(attr2)(self)))
        )


class TestMissingDataRemoveSeasonalityCUSUMDetectorModel(TestCase):
    def setUp(self) -> None:
        np.random.seed(0)
        x = np.random.normal(0.5, 3, 998)
        time_val0 = list(
            pd.date_range(start="2018-02-03 14:59:59", freq="1800s", periods=1000)
        )
        time_val = time_val0[:300] + time_val0[301:605] + time_val0[606:]
        self.tsd = TimeSeriesData(
            pd.DataFrame({"time": time_val, "value": pd.Series(x)})
        )

        time_val01 = list(
            pd.date_range(start="2018-02-03 14:00:04", freq="1800s", periods=1000)
        )
        time_val1 = time_val01[:300] + time_val01[301:605] + time_val01[606:]
        self.tsd1 = TimeSeriesData(
            pd.DataFrame({"time": time_val1, "value": pd.Series(x)})
        )


class TestRaiseCUSUMDetectorModel(TestCase):
    def setUp(self) -> None:
        np.random.seed(100)
        self.historical_window = 48 * 60 * 60  # in seconds
        self.scan_window = 24 * 60 * 60  # in seconds
        df_increase = pd.DataFrame(
            {
                "ts_value": np.concatenate(
                    [np.random.normal(1, 0.2, 156), np.random.normal(1.5, 0.2, 12)]
                ),
                "time": pd.date_range("2020-01-01", periods=168, freq="H"),
            }
        )

        self.tsd = TimeSeriesData(df_increase)

    def test_raise_direction(self) -> None:
        with self.assertRaisesRegex(
            InternalError, "direction can only be right or left"
        ):
            model = CUSUMDetectorModel(
                scan_window=self.scan_window, historical_window=self.historical_window
            )
            model._time2idx(self.tsd, self.tsd.time.iloc[0], "")

    def test_raise_model_instantiation(self) -> None:
        with self.assertRaisesRegex(
            ParameterError,
            "You must provide either serialized model or values for scan_window and historical_window.",
        ):
            _ = CUSUMDetectorModel()

    def test_raise_time_series_freq(self) -> None:
        with self.assertRaisesRegex(
            DataIrregularGranularityError, IRREGULAR_GRANULARITY_ERROR
        ):
            model = CUSUMDetectorModel(
                scan_window=self.scan_window, historical_window=self.historical_window
            )
            model.fit_predict(
                data=TimeSeriesData(
                    df=pd.DataFrame(
                        {
                            "value": [0] * 8,
                            "time": [
                                "2020-01-01",
                                "2020-01-02",
                                "2020-01-04",
                                "2020-01-07",
                                "2020-01-11",
                                "2020-01-16",
                                "2020-01-22",
                                "2020-01-29",
                            ],
                        }
                    )
                )
            )

    def test_raise_predict_not_implemented(self) -> None:
        with self.assertRaisesRegex(
            InternalError, r"predict is not implemented, call fit_predict\(\) instead"
        ):
            model = CUSUMDetectorModel(
                scan_window=self.scan_window, historical_window=self.historical_window
            )
            model.predict(data=self.tsd)


class TestDeltaReturnCUSUMDetectorModel(TestCase):
    def setUp(self) -> None:
        np.random.seed(100)
        self.scan_window = 24 * 60 * 60  # in seconds
        self.historical_window = 3 * 24 * 60 * 60  # in seconds
        self.test_data_window = 16  # in hours
        self.regression_sum_score = 12  #
        df_increase = pd.DataFrame(
            {
                "ts_value": np.concatenate(
                    [np.random.normal(1, 0.2, 156), np.random.normal(1.5, 0.2, 12)]
                ),
                "time": pd.date_range("2020-01-01", periods=168, freq="H"),
            }
        )
        self.tsd = TimeSeriesData(df_increase)
        self.tsd_value_name = self.tsd.value.name
        data = self.tsd[-self.test_data_window :]

        self.model = CUSUMDetectorModel(
            scan_window=self.scan_window, historical_window=self.historical_window
        )

        self.delta = self.model.fit_predict(
            data=data, historical_data=self.tsd[: -self.test_data_window]
        ).anomaly_magnitude_ts

    @parameterized.expand(
        [
            ("change_point_delta", len, "delta"),
        ]
    )
    def test_change_tsd(
        self,
        name: str,
        func_: Callable[[TimeSeriesData], float],
        attr1: str,
        # attr2: str,
    ) -> None:
        self.assertTrue(func_(attrgetter(attr1)(self)) > 0)


class TestCUSUMDetectorModelWindowsErrors(TestCase):
    def setUp(self) -> None:
        np.random.seed(100)
        control_time = pd.date_range(start="2018-01-06", freq="D", periods=(100))
        control_val = np.random.normal(0, 5, 100)
        self.data_ts = TimeSeriesData(time=control_time, value=pd.Series(control_val))

    def test_errors(self) -> None:
        # case 1: scan_window < 2 * frequency_sec
        model = CUSUMDetectorModel(
            scan_window=1 * 24 * 60 * 60, historical_window=2 * 24 * 60 * 60
        )
        with self.assertRaises(ParameterError):
            _ = model.fit_predict(data=self.data_ts)
        # case 2: historical_window < 2 * frequency_sec
        model = CUSUMDetectorModel(
            scan_window=2 * 24 * 60 * 60, historical_window=1 * 24 * 60 * 60
        )
        with self.assertRaises(ParameterError):
            _ = model.fit_predict(data=self.data_ts)
        # case 3: step_window < frequency_sec
        model = CUSUMDetectorModel(
            scan_window=5 * 24 * 60 * 60,
            historical_window=5 * 24 * 60 * 60,
            step_window=24 * 60 * 60 // 2,
        )
        with self.assertRaises(ParameterError):
            _ = model.fit_predict(data=self.data_ts)
        # case 4: step_window >= scan_window
        model = CUSUMDetectorModel(
            scan_window=5 * 24 * 60 * 60,
            historical_window=5 * 24 * 60 * 60,
            step_window=20 * 24 * 60 * 60,
        )
        with self.assertRaises(ParameterError):
            _ = model.fit_predict(data=self.data_ts)


class TestCUSUMDetectorModelChangeDirection(TestCase):
    def setUp(self) -> None:
        np.random.seed(100)
        control_time = pd.date_range(start="2018-01-06", freq="D", periods=(100))
        control_val = np.random.normal(0, 5, 100)
        self.data_ts = TimeSeriesData(time=control_time, value=pd.Series(control_val))

    def test_direction_list(self) -> None:
        model = CUSUMDetectorModel(
            scan_window=10 * 24 * 60 * 60,
            historical_window=10 * 24 * 60 * 60,
            threshold=0.01,
            delta_std_ratio=1.0,
            serialized_model=None,
            change_directions=["increase"],
            score_func=CusumScoreFunction.percentage_change,
        )
        anom = model.fit_predict(data=self.data_ts)
        self.assertEqual(len(anom.scores), len(self.data_ts))

    def test_direction_str(self) -> None:
        # case 1: scan_window < 2 * frequency_sec
        model = CUSUMDetectorModel(
            scan_window=10 * 24 * 60 * 60,
            historical_window=10 * 24 * 60 * 60,
            threshold=0.01,
            delta_std_ratio=1.0,
            serialized_model=None,
            change_directions="increase",
            score_func=CusumScoreFunction.percentage_change,
        )
        self.assertEqual(model.change_directions, ["increase"])
        anom = model.fit_predict(data=self.data_ts)
        self.assertEqual(len(anom.scores), len(self.data_ts))


class TestCUSUMDetectorModelIrregularGranularityError(TestCase):
    def setUp(self) -> None:
        np.random.seed(100)
        ts_time = list(
            pd.date_range(start="2018-01-06 00:00:00", freq="60s", periods=(100))
        )
        ts_time = ts_time[:60] + ts_time[61:80] + ts_time[81:]
        ts_time[82] = pd.to_datetime("2018-01-06 01:24:02")
        ts_time[85] = pd.to_datetime("2018-01-06 01:27:22")
        ts_val = np.random.normal(0, 5, 98)
        self.data_ts = TimeSeriesData(time=pd.Series(ts_time), value=pd.Series(ts_val))

    def test_irregular_granularity_error(self) -> None:
        model = CUSUMDetectorModel(
            scan_window=10 * 60,
            historical_window=10 * 60,
            threshold=0.01,
            delta_std_ratio=1.0,
            serialized_model=None,
            change_directions=["increase"],
            remove_seasonality=True,
        )

        with self.assertRaisesRegex(
            DataIrregularGranularityError,
            IRREGULAR_GRANULARITY_ERROR,
        ):
            _ = model.fit_predict(data=self.data_ts)


class TestVectorizedCUSUMDetectorModel(TestCase):
    def setUp(self) -> None:
        np.random.seed(0)
        val1 = np.random.normal(1, 0.2, 60)
        val1[50:] += 10
        val2 = np.random.normal(1, 0.2, 60)
        val2[40:] += 10
        val3 = np.random.normal(1, 0.2, 60)
        val3[45:] += 10
        self.y = pd.DataFrame(
            {
                "time": pd.Series(pd.date_range("2019-01-01", "2019-03-01")),
                "val1": val1,
                "val2": val2,
                "val3": val3,
            }
        )

    def test_percentage_change_results(self) -> None:
        tsmul = TimeSeriesData(self.y)

        for score_func, apm in [
            (CusumScoreFunction.percentage_change, True),
            (CusumScoreFunction.change, False),
            (CusumScoreFunction.z_score, False),
        ]:

            detector = VectorizedCUSUMDetectorModel(
                scan_window=3600 * 24 * 10,
                historical_window=3600 * 24 * 30,
                remove_seasonality=False,
                score_func=score_func,  # CusumScoreFunction.percentage_change | z_score | change
                adapted_pre_mean=apm,
            )
            cp1 = detector.fit_predict(tsmul)

            cp3 = {}
            cps_list = []
            alert_fired_list = []
            for col in tsmul.value.columns:
                d = CUSUMDetectorModel(
                    scan_window=3600 * 24 * 10,
                    historical_window=3600 * 24 * 30,
                    remove_seasonality=False,
                    score_func=score_func,  # CusumScoreFunction.percentage_change | z_score | change
                    adapted_pre_mean=apm,
                )
                cp3[col] = d.fit_predict(
                    TimeSeriesData(
                        value=tsmul.value[[col]],
                        time=pd.to_datetime(tsmul.time, unit="s", origin="unix"),
                    )
                )

                cps_list.append(d.cps)
                alert_fired_list.append(d.alert_fired)

            self.assertEqual(list(detector.cps), cps_list)
            self.assertEqual(list(detector.alert_fired), alert_fired_list)

            for col in ["val1", "val2", "val3"]:
                self.assertEqual(
                    (
                        round(cp3[col].scores.value, 10)
                        == round(cp1.scores.value.loc[:, col], 10)
                    ).sum(0),
                    60,
                )
                self.assertEqual(
                    (
                        round(cp3[col].anomaly_magnitude_ts.value, 10)
                        == round(cp1.anomaly_magnitude_ts.value.loc[:, col], 10)
                    ).sum(0),
                    60,
                )

    def test_seasonality_results(self) -> None:
        tsmul = TimeSeriesData(self.y)

        for score_func in [
            CusumScoreFunction.percentage_change,
            CusumScoreFunction.z_score,
        ]:

            detector = VectorizedCUSUMDetectorModel(
                scan_window=3600 * 24 * 10,
                historical_window=3600 * 24 * 30,
                remove_seasonality=True,
                score_func=score_func,
            )
            cp1 = detector.fit_predict(tsmul)

            cp3 = {}
            cps_list = []
            alert_fired_list = []
            for col in tsmul.value.columns:
                d = CUSUMDetectorModel(
                    scan_window=3600 * 24 * 10,
                    historical_window=3600 * 24 * 30,
                    remove_seasonality=True,
                    score_func=score_func,
                )
                cp3[col] = d.fit_predict(
                    TimeSeriesData(
                        value=tsmul.value[[col]],
                        time=pd.to_datetime(tsmul.time, unit="s", origin="unix"),
                    )
                )

                cps_list.append(d.cps)
                alert_fired_list.append(d.alert_fired)

            self.assertEqual(list(detector.cps), cps_list)
            self.assertEqual(list(detector.alert_fired), alert_fired_list)

            for col in ["val1", "val2", "val3"]:
                self.assertEqual(
                    (
                        round(cp3[col].scores.value, 10)
                        == round(cp1.scores.value.loc[:, col], 10)
                    ).sum(0),
                    60,
                )
                self.assertEqual(
                    (
                        round(cp3[col].anomaly_magnitude_ts.value, 10)
                        == round(cp1.anomaly_magnitude_ts.value.loc[:, col], 10)
                    ).sum(0),
                    60,
                )


class TestCallVectorizedCUSUM(TestCase):
    def setUp(self) -> None:
        np.random.seed(2)
        x = np.random.normal(0, 1, 110)
        x[25:] += 10
        x[50:] += 10
        x[80:] += 10
        freq = 86400
        start_time = pd.Timestamp("2019-01-01").value // 10**9
        y = pd.DataFrame(
            {
                "time": np.arange(start_time, start_time + 110 * freq, freq),
                "val1": x,
            }
        )
        y_irregular = pd.DataFrame(
            {
                "time": np.concatenate(
                    [
                        np.arange(start_time, start_time + 10 * freq, freq),
                        np.arange(
                            start_time + 12 * freq, start_time + 112 * freq, freq
                        ),
                    ]
                ),
                "val1": x,
            }
        )
        self.ts = TimeSeriesData(y, use_unix_time=True, unix_time_units="s")
        self.ts_tz_aware = TimeSeriesData(
            y, use_unix_time=True, unix_time_units="s", tz="US/Pacific"
        )
        self.ts_irregular = TimeSeriesData(
            y_irregular, use_unix_time=True, unix_time_units="s", tz="US/Pacific"
        )

    def test_vectorized_true_results(self) -> None:
        d = CUSUMDetectorModel(
            scan_window=3600 * 24 * 8,
            historical_window=3600 * 24 * 10,
            remove_seasonality=False,
            score_func=CusumScoreFunction.z_score,
            vectorized=False,
        )
        anom = d.fit_predict(data=self.ts[20:], historical_data=self.ts[:20])

        d1 = CUSUMDetectorModel(
            scan_window=3600 * 24 * 8,
            historical_window=3600 * 24 * 10,
            remove_seasonality=False,
            score_func=CusumScoreFunction.z_score,
            vectorized=True,
        )
        anom1 = d1.fit_predict(data=self.ts[20:], historical_data=self.ts[:20])

        self.assertEqual((anom1.scores.time == anom.scores.time).sum(0), 90)
        self.assertEqual(np.round(anom1.scores.value - anom.scores.value, 5).sum(0), 0)
        self.assertEqual(
            np.round(
                anom1.anomaly_magnitude_ts.value - anom.anomaly_magnitude_ts.value, 5
            ).sum(0),
            0,
        )
        self.assertTrue(np.round(anom1.scores.value, 5).sum(0) > 0)
        self.assertTrue(np.round(anom1.anomaly_magnitude_ts.value, 5).sum(0) > 0)
        self.assertEqual(
            (d.vectorized_trans_flag, d1.vectorized_trans_flag), (False, True)
        )

    def test_vectorized_true_results_tz_aware(self) -> None:
        d = CUSUMDetectorModel(
            scan_window=3600 * 24 * 8,
            historical_window=3600 * 24 * 10,
            remove_seasonality=False,
            score_func=CusumScoreFunction.z_score,
            vectorized=False,
        )
        anom = d.fit_predict(
            data=self.ts_tz_aware[20:], historical_data=self.ts_tz_aware[:20]
        )

        d1 = CUSUMDetectorModel(
            scan_window=3600 * 24 * 8,
            historical_window=3600 * 24 * 10,
            remove_seasonality=False,
            score_func=CusumScoreFunction.z_score,
            vectorized=True,
        )
        anom1 = d1.fit_predict(
            data=self.ts_tz_aware[20:], historical_data=self.ts_tz_aware[:20]
        )

        self.assertEqual((anom1.scores.time == anom.scores.time).sum(0), 90)
        self.assertEqual(np.round(anom1.scores.value - anom.scores.value, 5).sum(0), 0)
        self.assertEqual(
            np.round(
                anom1.anomaly_magnitude_ts.value - anom.anomaly_magnitude_ts.value, 5
            ).sum(0),
            0,
        )
        self.assertTrue(np.round(anom1.scores.value, 5).sum(0) > 0)
        self.assertTrue(np.round(anom1.anomaly_magnitude_ts.value, 5).sum(0) > 0)
        self.assertEqual(
            (d.vectorized_trans_flag, d1.vectorized_trans_flag), (False, True)
        )

    def test_vectorized_true_results_irregular_granularity(self) -> None:
        d = CUSUMDetectorModel(
            scan_window=3600 * 24 * 8,
            historical_window=3600 * 24 * 10,
            remove_seasonality=False,
            score_func=CusumScoreFunction.z_score,
            vectorized=False,
        )
        anom = d.fit_predict(
            data=self.ts_irregular[20:], historical_data=self.ts_irregular[:20]
        )

        d1 = CUSUMDetectorModel(
            scan_window=3600 * 24 * 8,
            historical_window=3600 * 24 * 10,
            remove_seasonality=False,
            score_func=CusumScoreFunction.z_score,
            vectorized=True,
        )
        anom1 = d1.fit_predict(
            data=self.ts_irregular[20:], historical_data=self.ts_irregular[:20]
        )

        self.assertEqual((anom1.scores.time == anom.scores.time).sum(0), 90)
        self.assertEqual(np.round(anom1.scores.value - anom.scores.value, 5).sum(0), 0)
        self.assertEqual(
            np.round(
                anom1.anomaly_magnitude_ts.value - anom.anomaly_magnitude_ts.value, 5
            ).sum(0),
            0,
        )
        self.assertTrue(np.round(anom1.scores.value, 5).sum(0) > 0)
        self.assertTrue(np.round(anom1.anomaly_magnitude_ts.value, 5).sum(0) > 0)
        # Can't use VectorizedCUSUMDetector for irregular granularity data
        self.assertEqual(
            (d.vectorized_trans_flag, d1.vectorized_trans_flag), (False, False)
        )

    def test_vectorized_true_seasonality_true_results(self) -> None:
        d = CUSUMDetectorModel(
            scan_window=3600 * 24 * 8,
            historical_window=3600 * 24 * 10,
            remove_seasonality=True,
            score_func=CusumScoreFunction.z_score,
            vectorized=False,
        )
        anom = d.fit_predict(data=self.ts[20:], historical_data=self.ts[:20])

        d1 = CUSUMDetectorModel(
            scan_window=3600 * 24 * 8,
            historical_window=3600 * 24 * 10,
            remove_seasonality=True,
            score_func=CusumScoreFunction.z_score,
            vectorized=True,
        )
        anom1 = d1.fit_predict(data=self.ts[20:], historical_data=self.ts[:20])

        self.assertEqual((anom1.scores.time == anom.scores.time).sum(0), 90)
        self.assertEqual(np.round(anom1.scores.value - anom.scores.value, 5).sum(0), 0)
        self.assertEqual(
            np.round(
                anom1.anomaly_magnitude_ts.value - anom.anomaly_magnitude_ts.value, 5
            ).sum(0),
            0,
        )
        self.assertTrue(np.round(anom1.scores.value, 5).sum(0) > 0)
        self.assertTrue(np.round(anom1.anomaly_magnitude_ts.value, 5).sum(0) > 0)
        self.assertEqual(
            (d.vectorized_trans_flag, d1.vectorized_trans_flag), (False, True)
        )

    def test_vetorized_delta_std_ratio_results(self) -> None:
        d = CUSUMDetectorModel(
            scan_window=3600 * 24 * 8,
            historical_window=3600 * 24 * 10,
            vectorized=False,
            delta_std_ratio=0.5,
        )
        anom = d.fit_predict(self.ts)

        d1 = CUSUMDetectorModel(
            scan_window=3600 * 24 * 8,
            historical_window=3600 * 24 * 10,
            vectorized=True,
            delta_std_ratio=0.5,
        )
        anom1 = d1.fit_predict(self.ts)

        self.assertEqual((anom1.scores.time == anom.scores.time).sum(0), 110)
        self.assertEqual(np.round(anom1.scores.value - anom.scores.value, 5).sum(0), 0)
        self.assertEqual(
            np.round(
                anom1.anomaly_magnitude_ts.value - anom.anomaly_magnitude_ts.value, 5
            ).sum(0),
            0,
        )
        self.assertTrue(np.round(anom1.scores.value, 5).sum(0) > 0)
        self.assertTrue(np.round(anom1.anomaly_magnitude_ts.value, 5).sum(0) > 0)


class CUSUMDetectorTest(TestCase):
    def setUp(self) -> None:
        np.random.seed(10)
        # increasing with variance detection setup
        df_increase = pd.DataFrame(
            {
                "increase": np.concatenate(
                    [np.random.normal(1, 0.2, 30), np.random.normal(1.5, 0.2, 30)]
                )
            }
        )

        df_increase["time"] = pd.Series(pd.date_range("2019-01-01", "2019-03-01"))
        inc_timeseries = TimeSeriesData(df_increase)
        self.inc_detector = CUSUMDetector(inc_timeseries)
        self.inc_change_points = self.inc_detector.detector()
        self.inc_metadata = self.inc_change_points[0]
        # decreasing detection setup
        df_decrease = pd.DataFrame(
            {
                "increase": np.concatenate(
                    [np.random.normal(1, 0.2, 30), np.random.normal(1.5, 0.2, 30)]
                )
            }
        )

        df_decrease["time"] = pd.Series(pd.date_range("2019-01-01", "2019-03-01"))

        dec_timeseries = TimeSeriesData(df_decrease)
        self.dec_detector = CUSUMDetector(dec_timeseries)
        self.dec_change_points = self.dec_detector.detector()
        self.dec_metadata = self.dec_change_points[0]
        # seasonality setup
        self.periodicity = 48
        self.total_cycles = 3
        harmonics = 2
        noise_std = 3

        seasonal_term = CUSUMDetectorTest.simulate_seasonal_term(
            self.periodicity,
            self.total_cycles,
            noise_std=noise_std,
            harmonics=harmonics,
        )
        seasonal_term = seasonal_term / seasonal_term.std() * 2
        residual = np.random.normal(0, 1, self.periodicity * self.total_cycles)
        self.seasonal_data = seasonal_term + residual
        # seasonality with increase trend setup
        trend_term = np.logspace(0, 1, self.periodicity * self.total_cycles)
        data = self.seasonal_data + trend_term
        data -= np.min(data)

        df_seasonality = pd.DataFrame(
            {
                "time": pd.date_range(
                    "2020-01-01",
                    periods=self.periodicity * self.total_cycles,
                    freq="30T",
                ),
                "seasonality": data,
            }
        )
        timeseries = TimeSeriesData(df_seasonality)
        self.season_inc_trend_detector = CUSUMDetector(timeseries)
        self.season_inc_trend_change_points = self.season_inc_trend_detector.detector(
            interest_window=[
                self.periodicity * (self.total_cycles - 1),
                self.periodicity * self.total_cycles - 1,
            ],
            magnitude_quantile=1,
            change_directions="both",
            delta_std_ratio=0,
        )
        self.season_metadata = self.season_inc_trend_change_points[0]
        # test on step change with no variance
        df_increase_no_var = pd.DataFrame(
            {
                "increase": np.concatenate(
                    [np.random.normal(1, 0, 30), np.random.normal(2, 0, 30)]
                )
            }
        )

        df_increase_no_var["time"] = pd.Series(
            pd.date_range("2019-01-01", "2019-03-01")
        )

        no_var_timeseries = TimeSeriesData(df_increase_no_var)
        self.no_var_detector = CUSUMDetector(no_var_timeseries)
        self.no_var_change_points = self.no_var_detector.detector()
        # no seasonality setup
        data = self.seasonal_data
        data -= np.min(data)

        df_seasonality = pd.DataFrame(
            {
                "time": pd.date_range(
                    "2020-01-01",
                    periods=self.periodicity * self.total_cycles,
                    freq="30T",
                ),
                "seasonality": data,
            }
        )
        timeseries = TimeSeriesData(df_seasonality)
        self.no_season_detector = CUSUMDetector(timeseries)
        self.no_season_change_points = self.no_season_detector.detector(
            interest_window=[
                self.periodicity * (self.total_cycles - 1),
                self.periodicity * self.total_cycles - 1,
            ],
            magnitude_quantile=1,
            change_directions=["increase"],
            delta_std_ratio=0,
        )
        # no regression setup
        df_noregress = pd.DataFrame({"no_change": np.random.normal(1, 0.2, 60)})

        df_noregress["time"] = pd.Series(pd.date_range("2019-01-01", "2019-03-01"))

        timeseries = TimeSeriesData(df_noregress)
        self.no_reg_detector = CUSUMDetector(timeseries)
        self.no_reg_change_points = self.no_reg_detector.detector(start_point=20)

    @parameterized.expand(
        [
            ["inc_change_points", 1],
            ["dec_change_points", 1],
            ["season_inc_trend_change_points", 1],
            ["no_var_change_points", 1],
            ["no_reg_change_points", 0],
            ["no_season_change_points", 0],
        ]
    )
    def test_cp_len(self, cp_name: str, expected: int) -> None:
        self.assertEqual(len(attrgetter(cp_name)(self)), expected)

    def test_increasing_mu(self) -> None:
        self.assertLess(self.inc_metadata.mu0, self.inc_metadata.mu1)

    def test_increasing_correct_delta(self) -> None:
        self.assertEqual(
            self.inc_metadata.delta, self.inc_metadata.mu1 - self.inc_metadata.mu0
        )

    def test_increasing_regression(self) -> None:
        self.assertTrue(self.inc_metadata.regression_detected)

    @parameterized.expand(
        [
            ["season_metadata.p_value_int", "season_metadata.llr_int"],
            ["inc_metadata.p_value", "inc_metadata.llr"],
        ]
    )
    def test_p_val(self, pval_name: str, llr_name: str) -> None:
        self.assertEqual(
            attrgetter(pval_name)(self),
            1 - chi2.cdf(attrgetter(llr_name)(self), 2),
        )

    def test_increasing_p_val_nan(self) -> None:
        self.assertTrue(np.isnan(self.inc_metadata.p_value_int))

    def test_increasing_llr_int(self) -> None:
        self.assertEqual(self.inc_metadata.llr_int, np.inf)

    def test_increasing_stable_changepoint(self) -> None:
        self.assertTrue(self.inc_metadata.stable_changepoint)

    @parameterized.expand(
        [
            ["inc_detector", "inc_change_points"],
            ["dec_detector", "dec_change_points"],
            ["season_inc_trend_detector", "season_inc_trend_change_points"],
            ["no_var_detector", "no_var_change_points"],
            ["no_reg_detector", "no_reg_change_points"],
            ["no_season_detector", "no_season_change_points"],
        ]
    )
    def test_plot(self, detector_name: str, cp_name: str) -> None:
        attrgetter(detector_name)(self).plot(attrgetter(cp_name)(self))

    @staticmethod
    def simulate_seasonal_term(
        periodicity: int,
        total_cycles: int,
        noise_std: float = 1.0,
        harmonics: Optional[float] = None,
    ) -> np.ndarray:
        duration = periodicity * total_cycles
        assert duration == int(duration)
        duration = int(duration)
        harmonics = harmonics if harmonics else int(np.floor(periodicity / 2))

        lambda_p = 2 * np.pi / float(periodicity)

        gamma_jt = noise_std * np.random.randn((harmonics))
        gamma_star_jt = noise_std * np.random.randn((harmonics))

        total_timesteps = 100 * duration  # Pad for burn in
        series = np.zeros(total_timesteps)
        for t in range(total_timesteps):
            gamma_jtp1 = np.zeros_like(gamma_jt)
            gamma_star_jtp1 = np.zeros_like(gamma_star_jt)
            for j in range(1, harmonics + 1):
                cos_j = np.cos(lambda_p * j)
                sin_j = np.sin(lambda_p * j)
                gamma_jtp1[j - 1] = (
                    gamma_jt[j - 1] * cos_j
                    + gamma_star_jt[j - 1] * sin_j
                    + noise_std * np.random.randn()
                )
                gamma_star_jtp1[j - 1] = (
                    -gamma_jt[j - 1] * sin_j
                    + gamma_star_jt[j - 1] * cos_j
                    + noise_std * np.random.randn()
                )
            series[t] = np.sum(gamma_jtp1)
            gamma_jt = gamma_jtp1
            gamma_star_jt = gamma_star_jtp1
        wanted_series = series[-duration:]  # Discard burn in

        return wanted_series

    def test_seasonality_with_increasing_trend_cp_index(self) -> None:
        self.assertGreaterEqual(
            self.season_metadata.cp_index,
            self.periodicity * (self.total_cycles - 1),
        )

    def test_logging_multivariate_error(self) -> None:
        # test multivariate error
        np.random.seed(10)
        df_multi_var = pd.DataFrame(
            {
                "no_change": np.random.normal(1, 0.2, 60),
                "no_change2": np.random.normal(1, 0.2, 60),
            }
        )

        df_multi_var["time"] = pd.Series(pd.date_range("2019-01-01", "2019-03-01"))

        with self.assertRaises(ValueError):
            timeseries = TimeSeriesData(df_multi_var)
            CUSUMDetector(timeseries)

    @parameterized.expand(
        [
            ["WARNING", 0.9],
            ["DEBUG", None],
        ]
    )
    def test_logging_neg_magnitude(self, level, mag_q) -> None:
        # test logging setup - negative in magnitude
        np.random.seed(10)
        df_neg = pd.DataFrame({"no_change": -np.random.normal(1, 0.2, 60)})

        df_neg["time"] = pd.Series(pd.date_range("2019-01-01", "2019-03-01"))

        timeseries = TimeSeriesData(df_neg)
        logging_detector = CUSUMDetector(timeseries)

        with self.assertLogs(level=level):
            logging_detector.detector(
                magnitude_quantile=mag_q, interest_window=[40, 60]
            )

    def test_ts_without_name(self) -> None:
        n = 10
        time = pd.Series(pd.date_range(start="2018-01-01", periods=n, freq="D"))
        value = pd.Series(np.arange(n))
        ts = TimeSeriesData(time=time, value=value)

        detector = CUSUMDetector(ts)
        change_points = detector.detector()
        detector.plot(change_points)


class MultiCUSUMDetectorTest(TestCase):
    def setUp(self) -> None:
        # increasing setup
        self.D = 10
        random_state = 10
        np.random.seed(random_state)
        mean1 = np.ones(self.D)
        mean2 = mean1 * 2
        sigma = make_spd_matrix(self.D, random_state=random_state)

        df_increase = pd.DataFrame(
            np.concatenate(
                [
                    np.random.multivariate_normal(mean1, sigma, 60),
                    np.random.multivariate_normal(mean2, sigma, 30),
                ]
            )
        )

        df_increase["time"] = pd.Series(pd.date_range("2019-01-01", "2019-04-01"))

        timeseries_increase = TimeSeriesData(df_increase)
        self.inc_change_points = MultiCUSUMDetector(timeseries_increase).detector()
        self.inc_metadata = self.inc_change_points[0]
        # decreasing setup
        df_decrease = pd.DataFrame(
            np.concatenate(
                [
                    np.random.multivariate_normal(mean2, sigma, 60),
                    np.random.multivariate_normal(mean1, sigma, 30),
                ]
            )
        )

        df_decrease["time"] = pd.Series(pd.date_range("2019-01-01", "2019-04-01"))

        timeseries_decrease = TimeSeriesData(df_decrease)
        self.dec_change_points = MultiCUSUMDetector(timeseries_decrease).detector()
        self.dec_metadata = self.dec_change_points[0]

    @parameterized.expand(
        [
            ["inc_change_points"],
            ["dec_change_points"],
        ]
    )
    def test_cp_len(self, cp_name: str) -> None:
        self.assertEqual(len(attrgetter(cp_name)(self)), 1)

    @parameterized.expand(
        [
            ["inc_metadata"],
            ["dec_metadata"],
        ]
    )
    def test_cp_index(self, cp_name: str) -> None:
        self.assertLessEqual(abs(attrgetter(cp_name)(self).cp_index - 59), 1)

    @parameterized.expand(
        [
            ["inc_metadata.mu0", "inc_metadata.mu1"],
            ["dec_metadata.mu1", "dec_metadata.mu0"],
        ]
    )
    def test_mu(self, m1_name: str, m2_name: str) -> None:
        for m1, m2 in zip(attrgetter(m1_name)(self), attrgetter(m2_name)(self)):
            self.assertLess(m1, m2)

    @parameterized.expand(
        [
            ["inc_metadata", "inc_metadata.mu0", "inc_metadata.mu1"],
            ["dec_metadata", "dec_metadata.mu0", "dec_metadata.mu1"],
        ]
    )
    def test_correct_delta(
        self, metadata_name: str, mu0_name: str, mu1_name: str
    ) -> None:
        for d, diff in zip(
            attrgetter(metadata_name)(self).delta,
            attrgetter(mu1_name)(self) - attrgetter(mu0_name)(self),
        ):
            self.assertEqual(d, diff)

    @parameterized.expand(
        [
            ["inc_metadata"],
            ["dec_metadata"],
        ]
    )
    def test_regression(self, metadata_name: str) -> None:
        self.assertTrue(attrgetter(metadata_name)(self).regression_detected)

    @parameterized.expand(
        [
            ["inc_metadata"],
            ["dec_metadata"],
        ]
    )
    def test_p_val(self, metadata_name: str) -> None:
        self.assertEqual(
            attrgetter(metadata_name)(self).p_value,
            1 - chi2.cdf(attrgetter(metadata_name)(self).llr, self.D + 1),
        )

    @parameterized.expand(
        [
            ["inc_metadata"],
            ["dec_metadata"],
        ]
    )
    def test_gaussian_increase_p_val_nan(self, metadata_name: str) -> None:
        self.assertTrue(np.isnan(attrgetter(metadata_name)(self).p_value_int))

    @parameterized.expand(
        [
            ["inc_metadata"],
            ["dec_metadata"],
        ]
    )
    def test_gaussian_increase_llr_int(self, metadata_name: str) -> None:
        self.assertEqual(attrgetter(metadata_name)(self).llr_int, np.inf)

    @parameterized.expand(
        [
            ["inc_metadata"],
            ["dec_metadata"],
        ]
    )
    def test_gaussian_increase_stable_changepoint(self, metadata_name: str) -> None:
        self.assertTrue(attrgetter(metadata_name)(self).stable_changepoint)

    def test_no_changepoint(self) -> None:
        D = 10
        random_state = 10
        np.random.seed(random_state)
        mean = np.ones(D)
        sigma = make_spd_matrix(D, random_state=random_state)
        # Use the same mean for the entire series and there should be no changepoint
        df_no_change = pd.DataFrame(np.random.multivariate_normal(mean, sigma, 90))
        df_no_change["time"] = pd.Series(pd.date_range("2019-01-01", "2019-04-01"))

        timeseries_no_change = TimeSeriesData(df_no_change)
        change_points = MultiCUSUMDetector(timeseries_no_change).detector()
        self.assertEqual(len(change_points), 0)


class VectorizedCUSUMDetectorTest(TestCase):
    def setUp(self) -> None:
        np.random.seed(10)
        # increasing with variance detection setup
        df = pd.DataFrame(
            {
                "increase": np.concatenate(
                    [np.random.normal(1, 0.2, 30), np.random.normal(1.5, 0.2, 30)]
                ),
                "decrease": np.concatenate(
                    [np.random.normal(1, 0.2, 50), np.random.normal(0.5, 0.2, 10)]
                ),
            }
        )
        df["time"] = pd.Series(pd.date_range("2019-01-01", "2019-03-01"))

        self.inc_change_points = CUSUMDetector(
            TimeSeriesData(df[["increase", "time"]])
        ).detector()
        self.dec_change_points = CUSUMDetector(
            TimeSeriesData(df[["decrease", "time"]])
        ).detector()
        self.dec_change_points_int_window = CUSUMDetector(
            TimeSeriesData(df[["decrease", "time"]])
        ).detector(change_directions="decrease", interest_window=(35, 55))

        timeseries = TimeSeriesData(df)
        change_points_vectorized_ = VectorizedCUSUMDetector(timeseries).detector_()
        # take the change points in all columns with the corresponding directions
        change_points_vectorized = [[], []]
        for i in range(len(change_points_vectorized_)):
            for change_points_ts in change_points_vectorized_[i]:
                if change_points_ts.direction == df.columns.values[i]:
                    change_points_vectorized[i].append(change_points_ts)
        # change points for the first column in the matrix
        self.inc_change_points_vectorized = change_points_vectorized[0]
        # change points for the second column in the matrix
        self.dec_change_points_vectorized = change_points_vectorized[1]

        self.dec_change_points_vectorized_int_window = VectorizedCUSUMDetector(
            timeseries
        ).detector_(change_directions=["decrease"], interest_window=(35, 55))[1]

    def test_vectorized_results(self) -> None:
        # check if vectorized CUSUM produces the same results with the original CUSUM
        self.assertEqual(
            self.inc_change_points[0].start_time,
            self.inc_change_points_vectorized[0].start_time,
        )
        self.assertEqual(
            len(self.inc_change_points),
            len(self.inc_change_points_vectorized),
        )
        self.assertEqual(
            self.dec_change_points[0].start_time,
            self.dec_change_points_vectorized[0].start_time,
        )
        self.assertEqual(
            len(self.dec_change_points),
            len(self.dec_change_points_vectorized),
        )
        self.assertEqual(
            self.dec_change_points_int_window[0].start_time,
            self.dec_change_points_vectorized_int_window[0].start_time,
        )
        self.assertEqual(
            len(self.dec_change_points_int_window),
            len(self.dec_change_points_vectorized_int_window),
        )

    def _comp_cpval(
        self,
        cps1: List[List[CUSUMChangePoint]],
        cps2: List[List[CUSUMChangePoint]],
        round_int: int = 10,
    ) -> bool:
        for i in range(len(cps1)):
            cp1 = cps1[i]
            cp2 = cps2[i]
            if len(cp1) != len(cp2):
                return False

            for j in range(len(cp1)):
                if cp1[j].almost_equal(cp2[j], round_int):
                    continue
                else:
                    return False

        return True

    def test_vectorized_detector_results(self) -> None:
        np.random.seed(0)
        y = pd.DataFrame(
            {
                "time": pd.Series(pd.date_range("2019-01-01", "2019-03-01")),
                "val1": np.random.normal(1, 0.2, 60),
                "val2": np.random.normal(1, 0.2, 60),
                "val3": np.random.normal(1, 0.2, 60),
            }
        )
        tsmul = TimeSeriesData(y)
        # interest_window = [20, 50]
        vcum = VectorizedCUSUMDetector(tsmul)
        res1 = vcum.detector(interest_window=[20, 50])

        res2 = []
        for i in range(0, y.shape[1] - 1):
            ts = TimeSeriesData(y.iloc[:, [0, i + 1]])
            detector = CUSUMDetector(ts)
            temp = detector.detector(interest_window=[20, 50])
            res2.append(temp)

        self.assertTrue(self._comp_cpval(res2, res1, 8))
        # interest_window = None
        vcum = VectorizedCUSUMDetector(tsmul)
        res1 = vcum.detector()

        res2 = []
        for i in range(0, y.shape[1] - 1):
            ts = TimeSeriesData(y.iloc[:, [0, i + 1]])
            detector = CUSUMDetector(ts)
            temp = detector.detector()
            res2.append(temp)

        self.assertTrue(self._comp_cpval(res2, res1, 8))
