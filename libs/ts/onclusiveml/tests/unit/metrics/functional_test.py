# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""Functional tests."""

# Standard Library
from typing import List, Optional, Union
from unittest import TestCase

# 3rd party libraries
import numpy as np
import numpy.testing as npt
from parameterized.parameterized import parameterized

# Internal libraries
from onclusiveml.ts.metrics import functional as F


class MetricsTest(TestCase):
    """Metrics test."""

    def validate(
        self, expected: Union[float, np.ndarray], result: Union[float, np.ndarray]
    ) -> None:
        """Validate assertion."""
        if isinstance(expected, float):
            self.assertTrue(isinstance(result, float))
            if np.isnan(expected):
                self.assertTrue(np.isnan(result), f"{result} is not nan")
            else:
                self.assertAlmostEqual(expected, result)
        else:
            self.assertTrue(isinstance(result, np.ndarray))
            npt.assert_array_almost_equal(np.array(expected), result)

    @parameterized.expand(
        [
            ("normal", [[1.0, 2.0], [3.0, 4.0]], [[1.0, 2.0], [3.0, 4.0]]),
            ("missing", [[1, 2], [2, 3]], [[1, 2], None, [2, 3]]),
            # TODO: nans
            ("empty", [], []),
        ]
    )
    def test__arrays(
        self, _name: str, expected: List[List[float]], arrs: List[List[float]]
    ) -> None:
        """Test array metric."""
        result = list(F._arrays(*arrs))
        self.assertEqual(len(expected), len(result))
        for e, a in zip(expected, result):
            npt.assert_almost_equal(np.array(e), a)

    def test__arrays_mismatched(self) -> None:
        """Test arrays mismatched."""
        with self.assertRaises(ValueError):
            _ = list(F._arrays([1], [2, 3]))

    @parameterized.expand(
        [
            ("normal", [0.25, 0.5, 2.0], [1, 2, 4], [4, 4, 2]),
            # TODO: more numerical combinations
        ]
    )
    def test__safe_divide(
        self,
        _name: str,
        exp: List[float],
        num: List[float],
        denom: Union[float, List[float]],
        negative_infinity: float = -1.0,
        positive_infinity: float = 1.0,
        indeterminate: float = 0.0,
        nan: float = np.nan,
    ) -> None:
        """Test safe divide."""
        expected = np.array(exp)
        numerator = np.array(num)
        denominator = np.array(denom)
        npt.assert_almost_equal(
            expected,
            F._safe_divide(
                numerator,
                denominator,
                negative_infinity,
                positive_infinity,
                indeterminate,
                nan,
            ),
        )

    @parameterized.expand(
        [
            ("normal", [-3, -2, 2], [1, 2, 4], [4, 4, 2]),
            ("weighted", [-1.25, -0.125, 0.375], [1, 2, 3], [3.5, 2.5, 1.5], [2, 1, 1]),
            # TODO: more numerical combinations
            ("empty", [], [], []),
        ]
    )
    def test_error(
        self,
        _name: str,
        expected: List[float],
        y_true: List[float],
        y_pred: List[float],
        weights: Optional[List[float]] = None,
    ) -> None:
        """Test error."""
        result = F.error(y_true, y_pred, weights)
        self.validate(np.array(expected), result)

    @parameterized.expand(
        [
            ("normal", [3, 2, 2], [1, 2, 4], [4, 4, 2]),
            ("weighted", [1.25, 0.125, 0.375], [1, 2, 3], [3.5, 2.5, 1.5], [2, 1, 1]),
            # TODO: more numerical combinations
            ("empty", [], [], []),
        ]
    )
    def test_absolute_error(
        self,
        _name: str,
        expected: List[float],
        y_true: List[float],
        y_pred: List[float],
        weights: Optional[List[float]] = None,
    ) -> None:
        """Test absolute error."""
        result = F.absolute_error(y_true, y_pred, weights)
        self.validate(np.array(expected), result)

    @parameterized.expand(
        [
            ("normal", [-3, -1, 0.5], [1, 2, 4], [4, 4, 2]),
            (
                "weighted",
                [-1.25, -0.0625, 0.125],
                [1, 2, 3],
                [3.5, 2.5, 1.5],
                [2, 1, 1],
            ),
            # TODO: more numerical combinations
            ("empty", [], [], []),
        ]
    )
    def test_percentage_error(
        self,
        _name: str,
        expected: List[float],
        y_true: List[float],
        y_pred: List[float],
        weights: Optional[List[float]] = None,
    ) -> None:
        """Test percentage error."""
        result = F.percentage_error(y_true, y_pred, weights)
        self.validate(np.array(expected), result)

    @parameterized.expand(
        [
            ("normal", [3, 1, 0.5], [1, 2, 4], [4, 4, 2]),
            ("weighted", [1.25, 0.0625, 0.125], [1, 2, 3], [3.5, 2.5, 1.5], [2, 1, 1]),
            # TODO: more numerical combinations
            ("empty", [], [], []),
        ]
    )
    def test_absolute_percentage_error(
        self,
        _name: str,
        expected: List[float],
        y_true: List[float],
        y_pred: List[float],
        weights: Optional[List[float]] = None,
    ) -> None:
        """Test absolute percentage error."""
        result = F.absolute_percentage_error(y_true, y_pred, weights)
        self.validate(np.array(expected), result)

    @parameterized.expand(
        [
            ("normal", 2 / 9, [1, 2, 4], [4, 4, 2]),
            # TODO: more numerical combinations
            ("all_pred_missing", np.nan, [1.0, 2.0], [np.nan, np.nan]),
            ("all_true_missing", 1.0, [np.nan, np.nan], [1.0, 2.0]),
            ("empty", np.nan, [], []),
        ]
    )
    def test_continuous_rank_probability_score(
        self,
        _name: str,
        expected: float,
        y_true: List[float],
        y_pred: List[float],
    ) -> None:
        """Test continuous rank probability score."""
        result = F.crps(y_true, y_pred)
        self.validate(expected, result)

    @parameterized.expand(
        [
            ("normal", 0.5, [2, 3, 4, -5], [1, 1, 1, 1], 3.0),
            ("empty", np.nan, [], [], 1.0),
        ]
    )
    def test_frequency_exceeds_relative_threshold(
        self,
        _name: str,
        expected: float,
        y_true: List[float],
        y_pred: List[float],
        threshold: float,
    ) -> None:
        """Test continuous rank probability score."""
        result = F.frequency_exceeds_relative_threshold(y_true, y_pred, threshold)
        self.validate(expected, result)

    @parameterized.expand(
        [
            ("normal", 4 / 9, [1, 2, 4], [4, 4, 2]),
            # TODO: more numerical combinations
            ("all_pred_missing", np.nan, [1.0, 2.0], [np.nan, np.nan]),
            ("all_true_missing", 1.0, [np.nan, np.nan], [1.0, 2.0]),
            ("empty", np.nan, [], []),
        ]
    )
    def test_linear_error_in_probability_space(
        self,
        _name: str,
        expected: float,
        y_true: List[float],
        y_pred: List[float],
    ) -> None:
        """Test linear error in probability space."""
        result = F.leps(y_true, y_pred)
        self.validate(expected, result)

    @parameterized.expand(
        [
            ("normal", 1.5, [1, 2, 3], [3.5, 2.5, 1.5]),
            # TODO: more numerical combinations
            ("empty", np.nan, [], []),
        ]
    )
    def test_median_absolute_error(
        self,
        _name: str,
        expected: float,
        y_true: List[float],
        y_pred: List[float],
    ) -> None:
        """Test median absolute error."""
        result = F.mdae(y_true, y_pred)
        self.validate(expected, result)

    @parameterized.expand(
        [
            ("normal", 0.5, [1, 2, 3], [3.5, 2.5, 1.5]),
            # TODO: more numerical combinations
            ("empty", np.nan, [], []),
        ]
    )
    def test_median_absolute_percent_error(
        self,
        _name: str,
        expected: float,
        y_true: List[float],
        y_pred: List[float],
    ) -> None:
        """Test MAP error."""
        result = F.mdape(y_true, y_pred)
        self.validate(expected, result)

    @parameterized.expand(
        [
            ("normal", 1.5, [1, 2, 3], [3.5, 2.5, 1.5]),
            ("weighted", 1.75, [1, 2, 3], [3.5, 2.5, 1.5], [2, 1, 1]),
            ("normal_2d", 2.25, [[1, 2, 3], [2, 4, 6]], [[3.5, 2.5, 1.5], [1, 1, 1]]),
            (
                "normal_2d_raw",
                [1.75, 1.75, 3.25],
                [[1, 2, 3], [2, 4, 6]],
                [[3.5, 2.5, 1.5], [1, 1, 1]],
                None,
                "raw_values",
            ),
            (
                "weighted_2d",
                2.458333333333,
                [[1, 2, 3], [2, 4, 6]],
                [[3.5, 2.5, 1.5], [1, 1, 1]],
                [[1, 1, 1], [1, 3, 1]],
            ),
            (
                "weighted_2d_raw",
                [1.75, 2.375, 3.25],
                [[1, 2, 3], [2, 4, 6]],
                [[3.5, 2.5, 1.5], [1, 1, 1]],
                [[1, 1, 1], [1, 3, 1]],
                "raw_values",
            ),
            # TODO: more numerical combinations
            ("empty", np.nan, [], []),
        ]
    )
    def test_mean_absolute_error(
        self,
        _name: str,
        expected: float,
        y_true: List[float],
        y_pred: List[float],
        weights: Optional[List[float]] = None,
        multioutput: Union[str, List[float]] = "uniform_average",
    ) -> None:
        """Test MAE metric."""
        result = F.mae(y_true, y_pred, weights, multioutput)
        self.validate(expected, result)

    def test_invalid_mean_absolute_error_multioutput(self) -> None:
        """Test invalud MAE."""
        with self.assertRaises(ValueError):
            _ = F.mae([], [], [], "mango")

    @parameterized.expand(
        [
            ("normal", 2.125 / 2, [-2, 2, 3, 4], [0.5, 2.5, 1.5, 0]),
            # TODO: more numerical combinations
            ("zero_baseline", np.nan, [1, 1, 1, 1], [3.5, 2.5, 1.5, 0]),
            ("empty", np.nan, [], []),
        ]
    )
    def test_mean_absolute_scaled_error(
        self,
        _name: str,
        expected: float,
        y_true: List[float],
        y_pred: List[float],
    ) -> None:
        """Test mean absolute scaled error."""
        result = F.mase(y_true, y_pred)
        self.validate(expected, result)

    @parameterized.expand(
        [
            ("normal", 1.0625, [1, 2, 3, 4], [3.5, 2.5, 1.5, 0]),
            # TODO: more numerical combinations
            ("empty", np.nan, [], []),
        ]
    )
    def test_mean_absolute_percent_error(
        self,
        _name: str,
        expected: float,
        y_true: List[float],
        y_pred: List[float],
    ) -> None:
        """Test mean absolute percentage error."""
        result = F.mape(y_true, y_pred)
        self.validate(expected, result)

    @parameterized.expand(
        [
            ("normal", 0.625, [1, 2, 3, 4], [3.5, 2.5, 1.5, 0]),
            # TODO: more numerical combinations
            ("empty", np.nan, [], []),
        ]
    )
    def test_mean_error(
        self,
        _name: str,
        expected: float,
        y_true: List[float],
        y_pred: List[float],
    ) -> None:
        """Test mean error."""
        result = F.me(y_true, y_pred)
        self.validate(expected, result)

    @parameterized.expand(
        [
            ("normal", -0.3125, [1, 2, 3, 4], [3.5, 2.5, 1.5, 0]),
            # TODO: more numerical combinations
            ("empty", np.nan, [], []),
        ]
    )
    def test_mean_percentage_error(
        self,
        _name: str,
        expected: float,
        y_true: List[float],
        y_pred: List[float],
    ) -> None:
        """Test mean percentage error."""
        result = F.mpe(y_true, y_pred)
        self.validate(expected, result)

    @parameterized.expand(
        [
            ("normal", 35 / 12, [1, 2, 3], [3.5, 2.5, 1.5]),
            ("weighted", 2.75, [1, 2, 3], [3.5, 2.5, 1.5], [1, 1, 2]),
            # TODO: more numerical combinations
            ("empty", np.nan, [], []),
        ]
    )
    def test_mean_squared_error(
        self,
        _name: str,
        expected: float,
        y_true: List[float],
        y_pred: List[float],
        weights: Optional[List[float]] = None,
    ) -> None:
        """Test mean squared error."""
        result = F.mse(y_true, y_pred, weights)
        self.validate(expected, result)

    @parameterized.expand(
        [
            ("normal", np.sqrt(35 / 12), [1, 2, 3], [3.5, 2.5, 1.5]),
            ("weighted", np.sqrt(2.75), [1, 2, 3], [3.5, 2.5, 1.5], [1, 1, 2]),
            # TODO: more numerical combinations
            ("empty", np.nan, [], []),
        ]
    )
    def test_root_mean_squared_error(
        self,
        _name: str,
        expected: float,
        y_true: List[float],
        y_pred: List[float],
        weights: Optional[List[float]] = None,
    ) -> None:
        """Test mean squared error."""
        result = F.rmse(y_true, y_pred, weights)
        self.validate(expected, result)

    @parameterized.expand(
        [
            ("normal", 0.5484140, [1, 2, 3], [3.5, 2.5, 1.5]),
            ("weighted", 0.5299002, [1, 2, 3], [3.5, 2.5, 1.5], [1, 1, 2]),
            # TODO: more numerical combinations
            ("empty", np.nan, [], []),
        ]
    )
    def test_root_mean_squared_log_error(
        self,
        _name: str,
        expected: float,
        y_true: List[float],
        y_pred: List[float],
        weights: Optional[List[float]] = None,
    ) -> None:
        """Test mean squared log error."""
        result = F.rmsle(y_true, y_pred, weights)
        self.validate(expected, result)

    @parameterized.expand(
        [
            ("normal", 1.4790199, [1, 2, 3], [3.5, 2.5, 1.5]),
            ("weighted", 0.3903124, [1, 2, 3], [3.5, 2.5, 1.5], [1, 1, 2]),
            # TODO: more numerical combinations
            ("empty", np.nan, [], []),
        ]
    )
    def test_root_mean_squared_percentage_error(
        self,
        _name: str,
        expected: float,
        y_true: List[float],
        y_pred: List[float],
        weights: Optional[List[float]] = None,
    ) -> None:
        """Test root mean squared percentage error."""
        result = F.rmspe(y_true, y_pred, weights)
        self.validate(expected, result)

    @parameterized.expand(
        [
            ("normal", 1 / 3, [1, 2, 3], [3.5, 2.5, 1.5]),
            # TODO: more numerical combinations
            ("empty", np.nan, [], []),
        ]
    )
    def test_scaled_symmetric_mean_absolute_percentage_error(
        self,
        _name: str,
        expected: float,
        y_true: List[float],
        y_pred: List[float],
    ) -> None:
        """Test scaled symmetric MAP error."""
        result = F.scaled_smape(y_true, y_pred)
        self.validate(expected, result)

    @parameterized.expand(
        [
            ("normal", 2 / 9, [1, 2, 3], [3.5, 2.5, 1.5]),
            ("negatives", 2 / 27, [-1, 2, 3], [3.5, 2.5, -1.5]),
            # TODO: more numerical combinations
            ("empty", np.nan, [], []),
        ]
    )
    def test_symmetric_bias(
        self,
        _name: str,
        expected: float,
        y_true: List[float],
        y_pred: List[float],
    ) -> None:
        """Test symmetric bias."""
        result = F.sbias(y_true, y_pred)
        self.validate(expected, result)

    @parameterized.expand(
        [
            ("normal", 2 / 3, [1, 2, 3], [3.5, 2.5, 1.5]),
            (
                "normal",
                0.673220686123912,
                [0.2, 0.2, 0.2, 0.8, 0.8],
                [0.0, 0.25, 0.5, 0.75, 1.0],
            ),
            # TODO: more numerical combinations
            ("empty", np.nan, [], []),
        ]
    )
    def test_symmetric_mean_absolute_percentage_error(
        self,
        _name: str,
        expected: float,
        y_true: List[float],
        y_pred: List[float],
    ) -> None:
        """Test symmetric MAP error."""
        result = F.smape(y_true, y_pred)
        self.validate(expected, result)

    @parameterized.expand(
        [
            ("normal", -1.0, [1, 2, 3], [3.5, 2.5, 1.5]),
            # TODO: more numerical combinations
            ("empty", np.nan, [], []),
        ]
    )
    def test_tracking_signal(
        self,
        _name: str,
        expected: float,
        y_true: List[float],
        y_pred: List[float],
    ) -> None:
        """Test tracking signal."""
        result = F.tracking_signal(y_true, y_pred)
        self.validate(expected, result)

    def test_metric(self) -> None:
        """Test metric."""
        self.assertEqual(F.mae, F.metric("mae"))
        with self.assertRaises(ValueError):
            _ = F.metric("mango")

    def test_core_metric(self) -> None:
        """Test core metric."""
        self.assertEqual(F.mae, F.core_metric("mae"))
        with self.assertRaises(ValueError):
            _ = F.metric("mango")

    @parameterized.expand(
        [
            (
                "normal",
                [0.4, 0.2, 0.33333333],
                [
                    (0.40547657, 0.21700191, -0.63343906, 0.24662161, -1.9395454),
                    (-0.04428768, 0.5543952, -0.40847492, -0.46409416, 0.4180088),
                    (-2.0893543, -0.12981987, -0.58653784, -0.58653784, 0.29072),
                ],
                [
                    (
                        -1.5253627,
                        -2.0157309,
                        -1.3632555,
                        1.8552899,
                        5.08259,
                        8.782536,
                        4.62253,
                        -0.73543787,
                        2.656838,
                        2.5200548,
                        9.273176,
                        2.6641555,
                        -0.39546585,
                        0.5721655,
                        -1.0635448,
                    ),
                    (
                        -3.8493829,
                        -3.2209146,
                        -2.5079165,
                        -1.3597498,
                        4.16947,
                        3.6076689,
                        3.6549635,
                        -1.8097634,
                        -0.76120234,
                        1.5070448,
                        4.0525684,
                        1.6184692,
                        -1.4960217,
                        -2.3242073,
                        -2.226036,
                    ),
                    (
                        -2.127775,
                        -2.4119477,
                        -0.58012056,
                        0.4478078,
                        3.292698,
                        5.592966,
                        2.9125519,
                        0.27569342,
                        1.0328965,
                        1.2424107,
                        6.086138,
                        1.2846599,
                        0.6023383,
                        -0.61473894,
                        -1.641422,
                    ),
                ],
                [0.05, 0.95, 0.99],
            ),
        ]
    )
    def test_mult_exceed(
        self,
        _name: str,
        expected: List[float],
        y_true: List[float],
        y_pred: List[float],
        threshold: List[float],
    ) -> None:
        """Test multivariate exceed."""
        result = F.mult_exceed(y_true, y_pred, threshold)
        self.validate(np.array(expected), result)

    @parameterized.expand(
        [
            ("normal", 1.3333333, [1, 5, 1], [5, 1, 1], 0),
            ("normal", 1.3333333, [1, 5, 1], [5, 1, 1], 0.5),
            ("normal", 1.3333333, [1, 5, 1], [5, 1, 1], 0.75),
            ("normal", 1.3333333, [1, 5, 1], [5, 1, 1], 1),
            # # TODO: more numerical combinations
            ("empty", np.nan, [], [], 1.0),
        ]
    )
    def test_pinball_loss(
        self,
        _name: str,
        expected: float,
        y_true: List[float],
        y_pred: List[float],
        threshold: float,
    ) -> None:
        """Test pinball loss."""
        result = F.pinball_loss(y_true, y_pred, threshold)
        self.validate(expected, result)

    @parameterized.expand(
        [
            (
                "normal",
                0.6,
                [
                    (0.40547657, 0.21700191, -0.63343906, 0.24662161, -1.9395454),
                    (-0.04428768, 0.5543952, -0.40847492, -0.46409416, 0.4180088),
                    (-2.0893543, -0.12981987, -0.58653784, -0.58653784, 0.29072),
                ],
                [
                    (-1.5253627, -2.0157309, -1.3632555, 1.8552899, 5.08259),
                    (-3.8493829, -3.2209146, -2.5079165, -1.3597498, 4.16947),
                    (-2.127775, -2.4119477, -0.58012056, 0.4478078, 3.292698),
                ],
                0.95,
            ),
            ("normal", 0.67, [1, 2, 3], [3.5, 2.5, 1.5], 0.25),
            ("normal", 0.67, [1, 2, 3], [3.5, 2.5, 1.5], 0.50),
            ("normal", 0.33, [1, 2, 3], [3.5, 2.5, 1.5], 0.75),
            ("empty", np.nan, [], [], 1.0),
        ]
    )
    def test_exceed(
        self,
        _name: str,
        expected: float,
        y_true: List[float],
        y_pred: List[float],
        threshold: float,
    ) -> None:
        """Test exceed."""
        result = F.exceed(y_true, y_pred, threshold)
        self.validate(expected, round(result, 2))

    @parameterized.expand(
        [
            ("normal", 0.33, [1.1, 2.0, 3.31], [1.2, 2.4, 3.3], [1.5, 2.2, 3.4]),
            ("empty", np.nan, [], [], []),
        ]
    )
    def test_coverage(
        self,
        _name: str,
        expected: float,
        y_true: List[float],
        y_lower: List[float],
        y_upper: List[float],
    ) -> None:
        """Test coverage score."""
        result = F.coverage(y_true, y_lower, y_upper)
        self.validate(expected, round(result, 2))

    @parameterized.expand(
        [
            (
                "normal",
                [0, 0, 1],
                [1.1, 2.0, 3.31],
                [1.2, 2.4, 3.3],
                [1.5, 2.2, 3.4],
                None,
            ),
            ("empty", [], [], [], [], None),
        ]
    )
    def test_mult_coverage(
        self,
        _name: str,
        expected: np.ndarray,
        y_true: List[float],
        y_lower: List[float],
        y_upper: List[float],
        rolling_window: Union[None, int],
    ) -> None:
        """Test multivariate coverage score."""
        result = F.mult_coverage(y_true, y_lower, y_upper, rolling_window)
        self.validate(expected, result)

    @parameterized.expand(
        [
            ("normal", 1.73, [1.1, 2.0, 3.31], [1.2, 2.4, 3.3], [1.5, 2.2, 3.4], 0.2),
            ("empty", np.nan, [], [], [], 0.2),
        ]
    )
    def interval_score(
        self,
        _name: str,
        expected: float,
        y_true: List[float],
        y_lower: List[float],
        y_upper: List[float],
        alpha: float,
    ) -> None:
        """Test interval score."""
        result = F.interval_score(y_true, y_lower, y_upper)
        self.validate(expected, round(result, 2))

    @parameterized.expand(
        [
            (
                "normal",
                [1.3, 3.8, 0.1],
                [1.1, 2.0, 3.31],
                [1.2, 2.4, 3.3],
                [1.5, 2.2, 3.4],
                0.2,
                None,
            ),
            ("empty", [], [], [], [], 0.2, None),
        ]
    )
    def test_mult_interval_score(
        self,
        _name: str,
        expected: np.ndarray,
        y_true: List[float],
        y_lower: List[float],
        y_upper: List[float],
        alpha: float,
        rolling_window: Union[None, int],
    ) -> None:
        """Test multiple interval score."""
        result = F.mult_interval_score(y_true, y_lower, y_upper, alpha, rolling_window)
        self.validate(expected, result)
