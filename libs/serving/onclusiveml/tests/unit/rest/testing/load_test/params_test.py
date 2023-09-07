"""Settings tests."""
# 3rd party libraries
import pytest
from locust import HttpUser, between, task
from pydantic import ValidationError

# Internal libraries
from onclusiveml.serving.rest.testing.load_test import (
    Criterion,
    EndpointReport,
    EnvironmentCriterion,
    EvaluatedCriteria,
    EvaluatedCriterion,
    LoadTestingParams,
    Measurement,
    Measurements,
    TestReport,
    ValidEndpointTypes,
    ValidMeasurements,
)


class TestWebsiteUser(HttpUser):
    """A test website user."""

    wait_time = between(1, 2)

    @task()
    def get_home_page(self):
        """Gets /."""
        self.client.get("/")


def test_load_testing_params_no_locust_file():
    """Tests the initialization of a LoadTestingParams using locust clients."""
    LoadTestingParams(locustfile="", user_classes=[TestWebsiteUser])


def test_load_testing_params_raise_no_locust_file():
    """Tests the raising of an error when falling back on default values."""
    with pytest.raises(FileNotFoundError):
        LoadTestingParams()


@pytest.mark.parametrize("test_measurement", ValidMeasurements.list())
def test_measurement(test_measurement):
    """Tests initialization of a Measurement instance."""
    Measurement(name=test_measurement, value=0.5)


def test_measurement_raise_invalid_name():
    """Tests the raising of an error when attempting an invalid measurement reference."""
    with pytest.raises(ValidationError):
        Measurement(name="invalid_metric_reference", value=0.1)


def test_measurements():
    """Tests the initialization of a Measurements instance."""
    Measurements(
        avg_response_time=Measurement(name="avg_response_time", value=0.5),
        # percentiles
        min_response_time=Measurement(name="min_response_time", value=0.5),
        response_time_p50=Measurement(name="response_time_p50", value=0.5),
        response_time_p55=Measurement(name="response_time_p55", value=0.5),
        response_time_p65=Measurement(name="response_time_p65", value=0.5),
        response_time_p75=Measurement(name="response_time_p75", value=0.5),
        response_time_p85=Measurement(name="response_time_p85", value=0.5),
        response_time_p90=Measurement(name="response_time_p90", value=0.5),
        response_time_p95=Measurement(name="response_time_p95", value=0.5),
        response_time_p99=Measurement(name="response_time_p99", value=0.5),
        max_response_time=Measurement(name="max_response_time", value=0.5),
        # # --- request counts&rates
        # all
        requests_total=Measurement(name="requests_total", value=0.5),
        requests_rps=Measurement(name="requests_rps", value=0.5),
        requests_rpm=Measurement(name="requests_rpm", value=0.5),
        # failure only
        failures_total=Measurement(name="failures_total", value=0.5),
        failures_percent=Measurement(name="failures_percent", value=0.5),
    )


def test_endpoint_report():
    """Tests the initialization of an EndpointReport instance.

    Also checks for the setting of the endpoint_id field via the root_validator.
    """
    test_endpoint_report = EndpointReport(
        endpoint_type="GET",
        endpoint_url="http://dummy_url",
        measurements=Measurements(
            avg_response_time=Measurement(name="avg_response_time", value=0.5),
            # percentiles
            min_response_time=Measurement(name="min_response_time", value=0.5),
            response_time_p50=Measurement(name="response_time_p50", value=0.5),
            response_time_p55=Measurement(name="response_time_p55", value=0.5),
            response_time_p65=Measurement(name="response_time_p65", value=0.5),
            response_time_p75=Measurement(name="response_time_p75", value=0.5),
            response_time_p85=Measurement(name="response_time_p85", value=0.5),
            response_time_p90=Measurement(name="response_time_p90", value=0.5),
            response_time_p95=Measurement(name="response_time_p95", value=0.5),
            response_time_p99=Measurement(name="response_time_p99", value=0.5),
            max_response_time=Measurement(name="max_response_time", value=0.5),
            # # --- request counts&rates
            # all
            requests_total=Measurement(name="requests_total", value=0.5),
            requests_rps=Measurement(name="requests_rps", value=0.5),
            requests_rpm=Measurement(name="requests_rpm", value=0.5),
            # failure only
            failures_total=Measurement(name="failures_total", value=0.5),
            failures_percent=Measurement(name="failures_percent", value=0.5),
        ),
    )
    # endpoint_id = {endpoint_type}_{endpoint_url}
    assert test_endpoint_report.endpoint_id == "GET_http://dummy_url"


def test_test_report():
    """Tests the initialization of a TestReport instance."""
    TestReport(
        completed={
            "GET_http://dummy_url": EndpointReport(
                endpoint_type="GET",
                endpoint_url="http://dummy_url",
                measurements=Measurements(
                    avg_response_time=Measurement(name="avg_response_time", value=0.5),
                    # percentiles
                    min_response_time=Measurement(name="min_response_time", value=0.5),
                    response_time_p50=Measurement(name="response_time_p50", value=0.5),
                    response_time_p55=Measurement(name="response_time_p55", value=0.5),
                    response_time_p65=Measurement(name="response_time_p65", value=0.5),
                    response_time_p75=Measurement(name="response_time_p75", value=0.5),
                    response_time_p85=Measurement(name="response_time_p85", value=0.5),
                    response_time_p90=Measurement(name="response_time_p90", value=0.5),
                    response_time_p95=Measurement(name="response_time_p95", value=0.5),
                    response_time_p99=Measurement(name="response_time_p99", value=0.5),
                    max_response_time=Measurement(name="max_response_time", value=0.5),
                    # # --- request counts&rates
                    # all
                    requests_total=Measurement(name="requests_total", value=0.5),
                    requests_rps=Measurement(name="requests_rps", value=0.5),
                    requests_rpm=Measurement(name="requests_rpm", value=0.5),
                    # failure only
                    failures_total=Measurement(name="failures_total", value=0.5),
                    failures_percent=Measurement(name="failures_percent", value=0.5),
                ),
            )
        },
        failures={},
        num_requests=10,
        num_requests_fail=5,
        start_time=1,
        end_time=2,
    )


@pytest.mark.parametrize("test_hard", [True, False])
@pytest.mark.parametrize("test_measurement", ValidMeasurements.list())
@pytest.mark.parametrize("test_ensure_lower", [True, False])
@pytest.mark.parametrize("test_endpoint_type", ValidEndpointTypes.list())
def test_criterion(test_measurement, test_endpoint_type, test_ensure_lower, test_hard):
    """Tests the initialization of a Critertion instance.

    Parametrized to try out
        - all valid measurements as defined in the ValidMeasurements class
        - all valid endpoint types as defined in the ValidEndpointTypes class
        - hard & soft type criterions
        - the-smaller-the-better & the-larger-the-better type criterions
    """
    Criterion(
        name=test_measurement,
        threshold=10,
        endpoint_type=test_endpoint_type,
        endpoint_url="http://dummy_url",
        ensure_lower=test_ensure_lower,
        hard=test_hard,
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
    """Tests the Criterion instance's was_met_in_measurement method.

    The criterion is evaluated against a selected set of Measurement instances using defined,
    boolean ground truth outcomes.
    """
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


@pytest.mark.parametrize(
    "test_measurement, test_threshold, test_ensure_lower, test_criteria_met_expected",
    [
        (ValidMeasurements.requests_rps.value, 3, False, False),
        (ValidMeasurements.requests_total.value, 1, False, True),
        (ValidMeasurements.failures_total.value, 4, True, False),
        (ValidMeasurements.avg_response_time.value, 6, True, True),
        (ValidMeasurements.response_time_p95.value, 0.05, True, False),
        (ValidMeasurements.response_time_p65.value, 0.05, True, True),
    ],
)
def test_criterion_was_met_in_report(
    test_measurement,
    test_threshold,
    test_ensure_lower,
    test_criteria_met_expected,
):
    """Tests the Criterion instance's was_met_in_report method.

    Evaluates it against a TestReport instance using defined,
    boolean ground truth outcomes.
    """
    test_report = TestReport(
        completed={
            "GET_http://dummy_url": EndpointReport(
                endpoint_type="GET",
                endpoint_url="http://dummy_url",
                measurements=Measurements(
                    avg_response_time=Measurement(name="avg_response_time", value=5.9),
                    # percentiles
                    min_response_time=Measurement(name="min_response_time", value=0.5),
                    response_time_p50=Measurement(name="response_time_p50", value=0.5),
                    response_time_p55=Measurement(name="response_time_p55", value=0.5),
                    response_time_p65=Measurement(
                        name="response_time_p65", value=0.049
                    ),
                    response_time_p75=Measurement(name="response_time_p75", value=0.5),
                    response_time_p85=Measurement(name="response_time_p85", value=0.5),
                    response_time_p90=Measurement(name="response_time_p90", value=0.5),
                    response_time_p95=Measurement(
                        name="response_time_p95", value=0.051
                    ),
                    response_time_p99=Measurement(name="response_time_p99", value=0.5),
                    max_response_time=Measurement(name="max_response_time", value=0.5),
                    # # --- request counts&rates
                    # all
                    requests_total=Measurement(name="requests_total", value=2),
                    requests_rps=Measurement(name="requests_rps", value=2.9),
                    requests_rpm=Measurement(name="requests_rpm", value=0.5),
                    # failure only
                    failures_total=Measurement(name="failures_total", value=5),
                    failures_percent=Measurement(name="failures_percent", value=0.5),
                ),
            )
        },
        failures={},
        num_requests=10,
        num_requests_fail=5,
        start_time=1,
        end_time=2,
    )

    criteria = Criterion(
        name=test_measurement,
        threshold=test_threshold,
        endpoint_url="http://dummy_url",
        ensure_lower=test_ensure_lower,
    )

    test_criteria_met_actual = criteria.was_met_in_report(test_report)

    assert test_criteria_met_actual == test_criteria_met_expected


def test_evaluated_criterion():
    """Tests the initialization of an EvaluatedCriterion instance."""
    EvaluatedCriterion(
        name=ValidMeasurements.failures_total.value,
        threshold=0.5,
        endpoint_url="http://dummy_url",
        ensure_lower=False,
        passed=True,
    )


def test_evaluated_criteria():
    """Tests the initialization of an EvaluatedCriteria instance."""
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


@pytest.mark.parametrize("test_measurement", ValidMeasurements.list())
@pytest.mark.parametrize("test_ensure_lower", [True, False])
@pytest.mark.parametrize("test_hard", [True, False])
@pytest.mark.parametrize("test_endpoint_type", ValidEndpointTypes.list())
def test_environment_criterion(
    test_measurement, test_hard, test_endpoint_type, test_ensure_lower
):
    """Tests the initialization of a EnvironmentCriterion instance.

    Parametrization tests the following cases:
        - all valid measurements as defined in the ValidMeasurements class
        - all valid endpoint types as defined in the ValidEndpointTypes class
        - hard & soft type criterions
        - the-smaller-the-better & the-larger-the-better type criterions
    """
    EnvironmentCriterion(
        name=test_measurement,
        threshold=10,
        hard=test_hard,
        endpoint_type=test_endpoint_type,
        endpoint_url="http://dummy_url",
        ensure_lower=test_ensure_lower,
    )
