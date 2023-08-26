"""Criteria tests."""
# Standard Library
import os

# 3rd party libraries
import pytest

# Internal libraries
from libs.serving.onclusiveml.serving.rest.testing.load_test import (
    Criterion,
    EndpointReport,
    EnvironmentCriterion,
    EvaluatedCriteria,
    LoadTestCriteria,
    Measurement,
    Measurements,
    TestReport,
    ValidEndpointTypes,
    ValidMeasurements,
)
from onclusiveml.serving import ServingBaseParams


def test_load_test_criteria():
    """Test LoadTestCriteria instanciation.

    Tests the initialization of a LoadTestCriteria instance passing actual
    criteria in the contructor, and checking for the resulting number of criteria
    being attached to the LoadTestCriteria instance.
    """
    test_criteria = [
        Criterion(
            name=ValidMeasurements.avg_response_time.value,
            threshold=10,
            endpoint_type=ValidEndpointTypes.delete.value,
            endpoint_url="http://dummy_url",
            ensure_lower=False,
        ),
        Criterion(
            name=ValidMeasurements.failures_percent.value,
            threshold=10,
            endpoint_type=ValidEndpointTypes.post.value,
            endpoint_url="http://dummy_url",
            ensure_lower=True,
        ),
    ]

    load_test_criteria = LoadTestCriteria(criteria=test_criteria)

    assert load_test_criteria.n_criteria == 2
    assert load_test_criteria.criteria == test_criteria


def test_load_test_criteria_generate_from_environment(
    test_serving_base_params_env_prefix,
):
    """Tests the generate_from_environment method of the LoadTestCriteria class.

    We export the required environment variables in the local test scope, and generate
    criteria by calling the method, and validate the resulting criteria against defined
    ground truth criteria attributes.
    """
    load_test_criteria = LoadTestCriteria()
    # export the variable specifying the number of environment criteria
    os.environ[f"{ServingBaseParams.__config__.env_prefix}n_criteria"] = "10"
    # export all indexed environment variables. Include the ones with default values to illustrate
    # what would go into the docker compose `environment` section. We set the non-default value
    # to make sure the environment variable is dictating the final field value, and not the default
    # settings
    for index in range(1, 11):
        os.environ[
            f"{ServingBaseParams.__config__.env_prefix}criteria_{index}_name"
        ] = "avg_response_time"
        os.environ[
            f"{ServingBaseParams.__config__.env_prefix}criteria_{index}_threshold"
        ] = "0.1"
        os.environ[
            f"{ServingBaseParams.__config__.env_prefix}criteria_{index}_endpoint_type"
        ] = "POST"
        os.environ[
            f"{ServingBaseParams.__config__.env_prefix}criteria_{index}_endpoint_url"
        ] = "http://dummy_url"
        os.environ[
            f"{ServingBaseParams.__config__.env_prefix}criteria_{index}_ensure_lower"
        ] = "no"
        os.environ[
            f"{ServingBaseParams.__config__.env_prefix}criteria_{index}_hard"
        ] = "no"

    load_test_criteria.generate_from_environment(n_criteria=10)

    assert load_test_criteria.n_criteria == 10

    for index, environment_criterion in zip(range(1, 11), load_test_criteria.criteria):
        assert isinstance(environment_criterion, EnvironmentCriterion)
        assert (
            environment_criterion.__config__.env_prefix
            == f"{test_serving_base_params_env_prefix}criteria_{index}_"  # noqa: W503
        )
        assert environment_criterion.name == "avg_response_time"
        assert environment_criterion.threshold == 0.1
        assert environment_criterion.endpoint_type == "POST"
        assert environment_criterion.endpoint_url == "http://dummy_url"
        assert environment_criterion.ensure_lower is False
        assert environment_criterion.hard is False


@pytest.mark.parametrize(
    "test_criteria, test_evaluated_criteria_passed_expected, test_evaluation_passed_expected",
    [
        (
            [
                Criterion(
                    name=ValidMeasurements.avg_response_time.value,
                    threshold=6,
                    endpoint_type=ValidEndpointTypes.get.value,
                    endpoint_url="http://dummy_url",
                    ensure_lower=True,
                    hard=True,
                ),
                Criterion(
                    name=ValidMeasurements.response_time_p50.value,
                    threshold=0.6,
                    endpoint_type=ValidEndpointTypes.get.value,
                    endpoint_url="http://dummy_url",
                    ensure_lower=True,
                    hard=True,
                ),
            ],
            (False, True),
            False,
        ),
        (
            [
                Criterion(
                    name=ValidMeasurements.avg_response_time.value,
                    threshold=6,
                    endpoint_type=ValidEndpointTypes.get.value,
                    endpoint_url="http://dummy_url",
                    ensure_lower=True,
                    hard=False,
                ),
                Criterion(
                    name=ValidMeasurements.failures_percent.value,
                    threshold=0.2,
                    endpoint_type=ValidEndpointTypes.get.value,
                    endpoint_url="http://dummy_url",
                    ensure_lower=True,
                    hard=True,
                ),
            ],
            (False, True),
            True,
        ),
    ],
)
def test_load_test_criteria_evaluate(
    test_criteria,
    test_evaluated_criteria_passed_expected,
    test_evaluation_passed_expected,
):
    """Tests the evaluate method of the LoadTestCriteria class.

    We call it on a TestReport instance, and validate the resulting EvaluatedCritera
    instance against defined ground truth criteria attributes, checking for:
        - overall evaluation outcome
        - individual criterion evaluation outcomes.
    """
    test_report = TestReport(
        completed={
            "GET_http://dummy_url": EndpointReport(
                endpoint_type="GET",
                endpoint_url="http://dummy_url",
                measurements=Measurements(
                    avg_response_time=Measurement(name="avg_response_time", value=7),
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
                    failures_percent=Measurement(name="failures_percent", value=0.1),
                ),
            )
        },
        failures={},
        num_requests=10,
        num_requests_fail=5,
        start_time=1,
        end_time=2,
    )

    load_test_criteria = LoadTestCriteria(criteria=test_criteria)

    test_evaluated_criteria = load_test_criteria.evaluate(test_report)

    assert isinstance(test_evaluated_criteria, EvaluatedCriteria)

    test_evaluated_criteria_passed_actual = (
        test_evaluated_criteria.evaluated_criteria[0].passed,
        test_evaluated_criteria.evaluated_criteria[1].passed,
    )

    test_evaluation_passed_actual = test_evaluated_criteria.passed
    # check that the individual criteria were evaluated correctly
    assert (
        test_evaluated_criteria_passed_actual == test_evaluated_criteria_passed_expected
    )
    # check that the overall evaluation - which considers whether a criteria is hard or soft - has
    # concluded correctly
    assert test_evaluation_passed_actual == test_evaluation_passed_expected
