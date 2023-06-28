# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.serving.rest.testing import (
    Criterion,
    EnvironmentCriterion,
    EvaluatedCriteria,
    EvaluatedCriterion,
    Measurement,
    ValidEndpointTypes,
    ValidMeasurements,
)


@pytest.mark.parametrize("test_measurement", ValidMeasurements.list())
def test_measurement(test_measurement):

    Measurement(name=test_measurement, value=0.5)


@pytest.mark.parametrize("test_measurement", ValidMeasurements.list())
@pytest.mark.parametrize("test_ensure_lower", [True, False])
@pytest.mark.parametrize("test_endpoint_type", ValidEndpointTypes.list())
def test_criterion(test_measurement, test_endpoint_type, test_ensure_lower):

    Criterion(
        name=test_measurement,
        threshold=10,
        endpoint_type=test_endpoint_type,
        endpoint_url="http://dummy_url",
        ensure_lower=test_ensure_lower,
    )


@pytest.mark.parametrize(
    "test_measurement, test_value, test_threshold, test_ensure_lower, test_criteria_met_expected",
    [
        (ValidMeasurements.requests_rps.value, 2, 3, False, False),
        (ValidMeasurements.requests_total.value, 2, 1, False, True),
        (ValidMeasurements.failures_total.value, 5, 4, True, False),
        (ValidMeasurements.avg_response_time.value, 5, 6, True, True),
        (ValidMeasurements.response_time_p95.value, 0.1, 0.05, True, False),
        (ValidMeasurements.response_time_p65.value, 0.01, 0.05, True, True),
    ],
)
def test_criterion_was_met_in_measurement(
    test_measurement,
    test_value,
    test_threshold,
    test_ensure_lower,
    test_criteria_met_expected,
):

    measurement = Measurement(
        name=test_measurement,
        value=test_value,
    )

    criteria = Criterion(
        name=test_measurement,
        threshold=test_threshold,
        endpoint_url="http://dummy_url",
        ensure_lower=test_ensure_lower,
    )

    test_criteria_met_actual = criteria.was_met_in_measurement(measurement)

    assert test_criteria_met_actual == test_criteria_met_expected


def test_evaluated_criterion():

    EvaluatedCriterion(
        name=ValidMeasurements.failures_total.value,
        threshold=0.5,
        endpoint_url="http://dummy_url",
        ensure_lower=False,
        passed=True,
    )


def test_evaluated_criteria():

    EvaluatedCriteria(
        evaluated_criteria=[
            EvaluatedCriterion(
                name=ValidMeasurements.requests_rpm.value,
                hard=True,
                threshold=0.5,
                endpoint_url="http://dummy_url",
                ensure_lower=False,
                passed=True,
            ),
            EvaluatedCriterion(
                name=ValidMeasurements.failures_total.value,
                hard=False,
                threshold=0.5,
                endpoint_url="http://dummy_url",
                ensure_lower=False,
                passed=False,
            ),
        ],
        passed=True,
    )


def test_environment_criterion():

    EnvironmentCriterion(
        name=ValidMeasurements.avg_response_time.value,
        threshold=10,
        endpoint_url="http://dummy_url",
    )
