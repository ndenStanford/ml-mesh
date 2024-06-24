"""Settings."""

# Standard Library
from typing import Any, Dict, List, Optional, Type

# 3rd party libraries
from locust import HttpUser
from locust.main import load_locustfile
from pydantic import field_validator, model_validator

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseModel, OnclusiveEnum
from onclusiveml.serving.params import ServingBaseParams


class LoadTestingParams(ServingBaseParams):
    """A configuration class defining the data model for the `LoadTest` class' `settings`.

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

    @model_validator(mode="before")
    def validate_client_behaviour_configurations(cls, values: Dict) -> Dict:
        """Validate client behaviour configurations."""
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


class ValidEndpointTypes(OnclusiveEnum):
    """A utility enum subclass to formally list all valid endpoint types."""

    get: str = "GET"
    post: str = "POST"
    put: str = "PUT"
    delete: str = "DELETE"


class ValidMeasurements(OnclusiveEnum):
    """Measurements enums.

    A utility enum subclass to formally list all valid load test metric names that the load test
    module supports. Useful when defining & validating Criterion instances.
    """

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


class BaseMeasurementValidator(OnclusiveBaseModel):
    """Base measurement field_validator.

    A parent params class meant for subclassing that implements validating a measurement name
    against the range of valid measurement names defined in ValidMeasurements.
    """

    name: str

    @field_validator("name")
    def check_valid_measurement(cls, value: str) -> str:
        """Check name against valid measurements."""
        if value not in ValidMeasurements.values():
            raise ValueError(
                f"Invalid measurement {value}. Must be one of "
                f"{ValidMeasurements.values()}."
            )

        return value


class BaseEndpointTypeValidator(OnclusiveBaseModel):
    """Base endpoint type field_validator.

    A parent params class meant for subclassing that implements validating a endpoint type
    against the range of valid endpoint types defined in ValidEndpointTypes.
    """

    endpoint_type: str = "GET"
    endpoint_url: str
    endpoint_id: str = ""

    @field_validator("endpoint_type")
    def check_valid_endpoint_type(cls, value: str) -> str:
        """Checks that endpoint type is valid."""
        if value not in ValidEndpointTypes.values():
            raise ValueError(
                f"Invalid endpoint type {value}. Must be one of "
                f"{ValidEndpointTypes.values()}."
            )

        return value

    @model_validator(mode="before")
    def set_request_id(cls, values: Dict) -> Dict:
        """Sets the request id."""
        print()
        print("======")
        print(values)
        print("======")
        print()
        values["endpoint_id"] = f"{values['endpoint_type']}_{values['endpoint_url']}"

        return values


class Measurement(BaseMeasurementValidator):
    """Simple params class implementing a measurement.

    Has:
        - a validated measurement name `name` field
        - a measurement `value` field
    """

    value: float


class Measurements(OnclusiveBaseModel):
    """Utility class to define data model for the load test measurements."""

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
    """Simple params wrapper around the Measurements params class."""

    measurements: Measurements


class TestReport(OnclusiveBaseModel):
    """A params class representing all data required for a fail/pass evaluation of a load test.

    An instance of this is generated by calling a LoadTest instance's `report` method (after having
    run a load test by calling its `run` method first).
    """

    completed: Dict[str, EndpointReport]
    failures: Dict
    num_requests: int
    num_requests_fail: int
    start_time: str
    end_time: str


class Criterion(BaseEndpointTypeValidator, BaseMeasurementValidator):
    """Utility class to define load testing success criteria."""

    threshold: float
    ensure_lower: bool = True
    # if True, failing this criterion as part of an EnvironmentCriteria assessment will fail the
    # entire test; otherwise, failing will simply emit a warning
    hard: bool = True

    def was_met_in_measurement(self, test_measurement: Measurement) -> bool:
        """Utility method to verify whether the criterion was met in a load test measurement.

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
        """Verifies whether the criterion was met in a load test.

        Utility method to verify whether the criterion was met in a load test by comparing the
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

            test_measurement_dict: Dict = all_measurements.model_dump().get(self.name)

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
    """Evaluated criterion data model.

    A simple params subclass of the Criterion class with the additional boolean `passed`
    attribute, representing the successful/failed evaluation outcome of this criterion against a
    TestReport instances.
    """

    passed: bool


class EvaluatedCriteria(OnclusiveBaseModel):
    """Evaluated creteria data model.

    A simple params class representing the outcome of calling a LoadTestCriteria instance's
    evaluate method on a TestReport instance, i.e. the params class representing a fully evaluated
    load test criteria set.

    Contains individual Criterion instances as well as their individual evaluation outcomes, and the
    overal evaluation outcome which is successfull if and only if each individual criterion with
    hard=True has been successfull.
    """

    evaluated_criteria: List[EvaluatedCriterion]
    passed: bool


class EnvironmentCriterion(ServingBaseParams, Criterion):
    """Criterion subclass that can be configured via environment variables.

    Used to auto-generate criteria objects with indexed environment prefixes to support
    the configuration of entire test requirements containing multiple criteria completely
    via environment variables.

    Useful for environment-only configuration of a LoadTestCriteria instance via its
    generate_from_environment method.
    """

    # to ensure validation errors for missing environment variables, we unset the default values for
    # all fields
    name: str
    threshold: float
    ensure_lower: bool
    hard: bool
    endpoint_type: str
    endpoint_url: str


class EnvironmentCriteriaCount(ServingBaseParams):
    """A simple params class to help set the number of EnvironmentCriterion instances."""

    n_criteria: int
