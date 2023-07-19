# -*- coding: utf-8 -*-

# Standard Library
from enum import Enum
from typing import Any, Dict, List, Optional, Type

# 3rd party libraries
from locust import HttpUser
from locust.main import load_locustfile
from pydantic import BaseModel, root_validator, validator

# Internal libraries
from libs.serving.onclusiveml.serving.params import ServingBaseParams


class LoadTestingParams(ServingBaseParams):
    """A configuration class defining the data model for the `LoadTest` class' `settings`
    constructor argument.

    Note: If a locustfile is being used to define client behaviour, that file must be available when
        instantiating a `LoadTestingParams` instance as it will be loaded during the validation
        stage of this pydantic BaseSetting subclass.

    """

    # --- load test client behaviour specification. Two options:
    # - customized classes (preferred), or
    # - reference to locustfile containing customized classes (not preferred - requires an
    #   additional 'external' file)
    user_classes: List[Type[HttpUser]] = []
    locustfile: str = "locustfile.py"
    # --- load test runner behaviour
    # size of locust client pool
    num_users: int = 1
    # per second spawn rate of clients until `num_users` is reached
    spawn_rate: float = 1
    # base url of the host
    host: str = ""
    # ?
    reset_stats: bool = False

    tags: Any = None
    exclude_tags: Any = None
    stop_timeout: Any = None
    # length of test - uses locust utilities to parse into numerical spec
    run_time: str = "20s"
    # log level of underlying locust processes
    loglevel: str = "INFO"

    @root_validator
    def validate_client_behaviour_configurations(cls, values: Dict) -> Dict:

        if not values["locustfile"] and not values["user_classes"]:

            raise ValueError(
                "Invalid client configuration: At least one of `locustfile` or "
                "`user_classes` fields must be specified."
            )

        elif values["locustfile"] and values["user_classes"]:

            raise ValueError(
                "Invalid client configuration: Only one of `locustfile` or "
                "`user_classes` fields must be specified."
            )

        elif values["locustfile"]:

            docstring, classes, shape_class = load_locustfile(values["locustfile"])
            values["user_classes"] = [classes[n] for n in classes]

        return values


class ValidEndpointTypes(Enum):

    get: str = "GET"
    post: str = "POST"
    put: str = "PUT"
    delete: str = "DELETE"

    @classmethod
    def list(cls) -> List[str]:

        valid_endpoint_types = [
            valid_endpoint_type.value for valid_endpoint_type in cls
        ]

        return valid_endpoint_types


class ValidMeasurements(Enum):
    # --- latency
    avg_response_time: str = "avg_response_time"
    # percentiles
    min_response_time: str = "min_response_time"
    response_times: str = "response_times"
    response_time_p50: str = "response_time_p50"
    response_time_p55: str = "response_time_p55"
    response_time_p65: str = "response_time_p65"
    response_time_p75: str = "response_time_p75"
    response_time_p85: str = "response_time_p85"
    response_time_p90: str = "response_time_p90"
    response_time_p95: str = "response_time_p95"
    response_time_p99: str = "response_time_p99"
    max_response_time: str = "max_response_time"
    # --- request counts&rates
    # all
    requests_total: str = "requests_total"
    requests_rps: str = "requests_rps"
    requests_rpm: str = "requests_rpm"
    # failure only
    failures_total: str = "failures_total"
    failures_percent: str = "failures_percent"

    @classmethod
    def list(cls) -> List[str]:

        valid_measurements = [valid_measurement.value for valid_measurement in cls]

        return valid_measurements


class BaseMeasurementValidator(BaseModel):

    name: str

    @validator("name")
    def check_valid_measurement(cls, value: str) -> str:

        if value not in ValidMeasurements.list():
            raise ValueError(
                f"Invalid measurement {value}. Must be one of "
                f"{ValidMeasurements.list()}."
            )

        return value


class BaseEndpointTypeValidator(BaseModel):

    endpoint_type: str = "GET"
    endpoint_url: str
    endpoint_id: str = ""

    @validator("endpoint_type")
    def check_valid_endpoint_type(cls, value: str) -> str:

        if value not in ValidEndpointTypes.list():
            raise ValueError(
                f"Invalid endpoint type {value}. Must be one of "
                f"{ValidEndpointTypes.list()}."
            )

        return value

    @root_validator
    def set_request_id(cls, values: Dict) -> Dict:

        values["endpoint_id"] = f"{values['endpoint_type']}_{values['endpoint_url']}"

        return values


class Measurement(BaseMeasurementValidator):
    value: float


class Measurements(BaseModel):
    """Utility class to define data model for the load test measurements of a given endpoint &
    request type."""

    # --- latency
    # average
    avg_response_time: Measurement
    # percentiles
    min_response_time: Measurement
    response_time_p50: Measurement
    response_time_p55: Measurement
    response_time_p65: Measurement
    response_time_p75: Measurement
    response_time_p85: Measurement
    response_time_p90: Measurement
    response_time_p95: Measurement
    response_time_p99: Measurement
    max_response_time: Measurement
    # # --- request counts&rates
    # all
    requests_total: Measurement
    requests_rps: Measurement
    requests_rpm: Measurement
    # failure only
    failures_total: Measurement
    failures_percent: Measurement


class EndpointReport(BaseEndpointTypeValidator):

    measurements: Measurements


class TestReport(BaseModel):

    completed: Dict[str, EndpointReport]
    failures: Dict
    num_requests: int
    num_requests_fail: int
    start_time: str
    end_time: str


class Criterion(BaseEndpointTypeValidator, BaseMeasurementValidator):
    """Utility class to define load testing success criteria based on quantitative latency
    and response type metrics."""

    threshold: float
    ensure_lower: bool = True

    # if True, failing this criterion as part of an EnvironmentCriteria assessment will fail the
    # entire test; otherwise, failing will simply emit a warning
    hard: bool = True

    def was_met_in_measurement(self, test_measurement: Measurement) -> bool:
        """Utility method to verify whether the criterion was met in a load test measuremebt by
        comparing the threshold against the observed value of the specified Measurement instance

        Args:
            test_measurement (Measurement): The measurement (i.e. observation) that is being
                evaluated against the criterion

        Raises:
            ValueError: If the criterion's name does not match the specified test report's name, a
                ValueError is raised.

        Returns:
            bool: Whether the criterion was met in the specified Measurement
        """

        if self.name != test_measurement.name:
            raise ValueError(
                f"The criterion's name {self.name} does not match the measurement's "
                f"name {test_measurement.name}. Please make sure you are applying "
                "this criterion to the correct measurement"
            )

        is_lower = test_measurement.value < self.threshold
        criteria_was_met = is_lower == self.ensure_lower

        return criteria_was_met

    def was_met_in_report(self, test_report: TestReport) -> bool:
        """Utility method to verify whether the criterion was met in a load test by comparing the
        threshold against the observed value of the relevant measurement, picked out from a
        specified TestReport instance

        Args:
            test_report (TestReport): The TestReport instance as returned by a LocusLoadTest's
                `report` method.

        Raises:
            ValueError: If the criterion's endpoint report is available but is missing the
                criterion's measurement, this exeception is raised. This indicates that Locust was
                able to perform a load test successfully, but did not collect the measurement needed
                to evaluate this criterion.

                Note that if the entire endpoint report for the criterion's endpoint id could not be
                found, we return `False`.

        Returns:
            bool: Whether the criterion was met in the specified TestReport.
        """

        endpoint_report: Optional[EndpointReport] = test_report.completed.get(
            self.endpoint_id
        )

        if endpoint_report is not None:
            # if the corresponding endpoint report is available, try and extract the specified
            # measurement
            all_measurements = endpoint_report.measurements

            test_measurement_dict: Dict = all_measurements.dict().get(self.name)

            if test_measurement_dict is None:
                raise ValueError(
                    f"The specified measure {self.name} could not be found in the "
                    f"endpoint report for id {self.endpoint_id}. Are you sure these "
                    "specs are correct?"
                )
            else:
                test_measurement = Measurement(**test_measurement_dict)

            criteria_was_met = self.was_met_in_measurement(test_measurement)

        else:
            # A failed endpoint scenario would mean the entire endpoint report would be missing,
            # from the TestReport, so in those cases returning False would be a sensible evaluation
            # outcome against a measurement that could not be taken due to more fundamental issues.
            criteria_was_met = False

        return criteria_was_met


class EvaluatedCriterion(Criterion):

    passed: bool


class EvaluatedCriteria(BaseModel):

    evaluated_criteria: List[EvaluatedCriterion]
    passed: bool


class EnvironmentCriterion(ServingBaseParams, Criterion):
    """Criterion subclass that can be configured via environment variables. Used to auto-generate
    criteria objects with indexed environment prefixes to support the configuration of entire
    test requirements containing multiple criteria completely via environment variables."""

    # to ensure validation errors for missing environment variables, we unset the default values for
    # all fields
    name: str
    threshold: float
    ensure_lower: bool
    hard: bool
    endpoint_type: str
    endpoint_url: str


class EnvironmentCriteriaCount(ServingBaseParams):

    n_criteria: int
