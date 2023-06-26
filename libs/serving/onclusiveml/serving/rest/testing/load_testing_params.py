# -*- coding: utf-8 -*-

# Standard Library
from enum import Enum
from typing import Any, Dict, List, Optional, Type

# 3rd party libraries
from locust import HttpUser
from locust.main import load_locustfile
from pydantic import BaseModel, root_validator, validator

# Internal libraries
from onclusiveml.serving.rest.serving_base_params import ServingBaseParams


class LoadTestingParams(ServingBaseParams):
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


class BaseMeasurementValidator(BaseModel):

    name: str
    value: float

    @validator("name")
    def check_valid_measurement(cls, value: str) -> str:

        valid_measurements = [
            valid_measurement.value for valid_measurement in ValidMeasurements
        ]

        if value not in valid_measurements:
            raise ValueError(
                f"Invalid measurement {value}. Must be one of " f"{valid_measurements}."
            )

        return value

    @validator("value")
    def check_valid_rate_or_latency(cls, value: float) -> float:

        if value < 0:
            raise ValueError(
                f"Invalid value for observed latency or rate metric: {value}. Must be"
                "0 or greater."
            )

        return value


class BaseEndpointTypeValidator(BaseModel):

    endpoint_type: str = "GET"
    endpoint_url: str
    endpoint_id: str = ""

    @validator("endpoint_type")
    def check_valid_target_measurement(cls, value: str) -> str:

        valid_endpoint_types = [
            valid_endpoint_type.value for valid_endpoint_type in ValidEndpointTypes
        ]

        if value not in valid_endpoint_types:
            raise ValueError(
                f"Invalid endpoint type {value}. Must be one of "
                f"{valid_endpoint_types}."
            )

        return value

    @root_validator
    def set_request_id(cls, values: Dict) -> Dict:

        values["endpoint_id"] = f"{values['endpoint_type']}_{values['endpoint_url']}"

        return values


class Measurement(BaseMeasurementValidator):
    pass


class PercentileMeasurement(BaseMeasurementValidator):
    percentile: float

    @validator("percentile")
    def check_percentile(cls, value: float) -> float:

        if not (0 < value and value < 1):
            raise ValueError(
                f"Invalid percentile: {value}. Percentile level needs to be (0,1)."
            )

        return value


class Measurements(BaseModel):
    """Utility class to define data model for the load test measurements of a given endpoint &
    request type."""

    # --- latency
    # average
    avg_response_time: Measurement
    # percentiles
    min_response_time: Measurement
    response_time_p50: PercentileMeasurement
    response_time_p55: PercentileMeasurement
    response_time_p65: PercentileMeasurement
    response_time_p75: PercentileMeasurement
    response_time_p85: PercentileMeasurement
    response_time_p90: PercentileMeasurement
    response_time_p95: PercentileMeasurement
    response_time_p99: PercentileMeasurement
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


class Criteria(BaseEndpointTypeValidator, BaseMeasurementValidator):
    """Utility class to define load testing success criteria based on quantitative latency
    and response type metrics."""

    threshold: float
    ensure_lower: bool = True

    def was_met(self, test_report: TestReport) -> bool:
        """Utility method to verify whether the criteria was met in a load test by comparing the
        threshold against the observed value of the relevant measurement, picked out from a
        dictionary of type (endpoint_id, stat_for_that_endpoint_id)"""

        endpoint_report: Optional[EndpointReport] = test_report.completed.get(
            self.endpoint_id
        )

        if endpoint_report is not None:
            # if the corresponding endpoint report is available, try and extract the specified
            # measurement
            all_measurements = endpoint_report.measurements
            relevant_measurement: Optional[Measurement] = all_measurements.dict().get(
                self.endpoint_id
            )

            if relevant_measurement is None:
                raise ValueError(
                    f"The specified measure {self.name} could not be found in the "
                    f"endpoint report for id {self.endpoint_id}. Are you sure these "
                    "specs are correct?"
                )

            criteria_was_met = bool(
                self.ensure_lower * (self.threshold < relevant_measurement.value)
            )

        else:
            # criteria couldnt be found, we will return False for now. A failed endpoint scenario
            # would mean the entire endpoint report would be missing, so in those cases this would
            # be sensible default behaviour.
            criteria_was_met = False

        return criteria_was_met
