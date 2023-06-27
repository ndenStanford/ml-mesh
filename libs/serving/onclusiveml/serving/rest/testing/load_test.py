# -*- coding: utf-8 -*-
# Taken directly from https://github.com/FutureSharks/invokust with minimal changes under the MIT
# licence: https://github.com/FutureSharks/invokust/blob/master/LICENSE

# Standard Library
import logging
import signal
import sys
import time

# 3rd party libraries
import gevent
from locust.env import Environment
from locust.log import setup_logging
from locust.stats import stats_printer
from locust.util.timespan import parse_timespan

# Internal libraries
from onclusiveml.serving.rest.testing import (
    EndpointReport,
    LoadTestingParams,
    Measurement,
    Measurements,
    TestReport,
)


setup_logging("INFO", None)
logger = logging.getLogger(__name__)


def sig_term_handler() -> None:
    logger.info("Got SIGTERM signal")
    sys.exit(0)


class LocustLoadTest(object):
    """
    Runs a Locust load test and generates a qantitative report that integrates with the
    `Criteria` class from the `load_testing_params` module.
    """

    def __init__(self, settings: LoadTestingParams):
        self.settings = settings
        self.start_time: float = -1
        self.end_time: float = -1
        gevent.signal_handler(signal.SIGTERM, sig_term_handler)

    def report(self) -> TestReport:
        """
        Returns the statistics from the load test in JSON
        """
        test_report = {
            "completed": {},
            "failures": {},
            "num_requests": self.env.runner.stats.num_requests,
            "num_requests_fail": self.env.runner.stats.num_failures,
            "start_time": self.start_time,
            "end_time": self.end_time,
        }

        for endpoint_test_result in self.env.runner.stats.entries.values():

            endpoint_url = endpoint_test_result.name
            endpoint_type = endpoint_test_result.method
            endpoint_id = f"{endpoint_type}_{endpoint_url}"

            test_report["completed"][endpoint_id] = EndpointReport(
                endpoint_url=endpoint_url,
                endpoint_type=endpoint_type,
                measurements=Measurements(
                    avg_response_time=Measurement(
                        name="avg_response_time",
                        value=endpoint_test_result.avg_response_time,
                    ),
                    # latency min
                    min_response_time=Measurement(
                        name="min_response_time",
                        value=endpoint_test_result.min_response_time,
                    ),
                    # latency percentiles
                    response_time_p50=Measurement(
                        name="response_time_p50",
                        value=endpoint_test_result.get_response_time_percentile(0.50),
                    ),
                    response_time_p55=Measurement(
                        name="response_time_p55",
                        value=endpoint_test_result.get_response_time_percentile(0.55),
                    ),
                    response_time_p65=Measurement(
                        name="response_time_p65",
                        value=endpoint_test_result.get_response_time_percentile(0.65),
                    ),
                    response_time_p75=Measurement(
                        name="response_time_p75",
                        value=endpoint_test_result.get_response_time_percentile(0.75),
                    ),
                    response_time_p85=Measurement(
                        name="response_time_p85",
                        value=endpoint_test_result.get_response_time_percentile(0.85),
                    ),
                    response_time_p90=Measurement(
                        name="response_time_p90",
                        value=endpoint_test_result.get_response_time_percentile(0.90),
                    ),
                    response_time_p95=Measurement(
                        name="response_time_p95",
                        value=endpoint_test_result.get_response_time_percentile(0.95),
                    ),
                    response_time_p99=Measurement(
                        name="response_time_p99",
                        value=endpoint_test_result.get_response_time_percentile(0.90),
                    ),
                    # latency max
                    max_response_time=Measurement(
                        name="max_response_time",
                        value=endpoint_test_result.max_response_time,
                    ),
                    # --- request counts&rates
                    # all
                    requests_total=Measurement(
                        name="requests_total", value=endpoint_test_result.num_requests
                    ),
                    requests_rps=Measurement(
                        name="requests_rps", value=endpoint_test_result.total_rps
                    ),
                    requests_rpm=Measurement(
                        name="requests_rpm",
                        value=endpoint_test_result.total_rps * 60,
                    ),
                    # # failure only
                    failures_total=Measurement(
                        name="failures_total", value=endpoint_test_result.num_failures
                    ),
                    failures_percent=Measurement(
                        name="failures_percent",
                        value=endpoint_test_result.num_failures
                        / endpoint_test_result.num_requests,  # noqa: W503
                    ),
                ),
            )

        for _, error in self.env.runner.errors.items():
            error_dict = error.serialize()
            locust_task_name = "{0}_{1}".format(
                error_dict["method"], error_dict["name"]
            )
            test_report["failures"][locust_task_name] = error_dict
        # cast as data model
        test_report_validated = TestReport(**test_report)

        return test_report_validated

    def set_run_time_in_sec(self, run_time_str: str) -> None:
        try:
            self.run_time_in_sec = parse_timespan(run_time_str)
        except ValueError:
            logger.error(
                f"Invalid format for `run_time` parameter: '{run_time_str}', "
                "Valid formats are: 20s, 3m, 2h, 1h20m, 3h30m10s, etc."
            )
            sys.exit(1)
        except TypeError:
            logger.error(
                f"`run_time` must be a string, not {type(run_time_str)}. Received value: "
                f"{run_time_str} "
            )
            sys.exit(1)

    def run(self) -> None:
        """
        Run the load test.
        """

        if self.settings.run_time:
            self.set_run_time_in_sec(run_time_str=self.settings.run_time)

            logger.info(f"Run time limit set to {self.run_time_in_sec} seconds")

            def timelimit_stop() -> None:
                logger.info(
                    f"Run time limit reached: {self.run_time_in_sec} seconds. Stopping Locust "
                    "Runner."
                )
                self.env.runner.quit()
                self.end_time = time.time()
                logger.info(
                    f"Locust completed {self.env.runner.stats.num_requests} requests with "
                    f"{len(self.env.runner.errors)} errors"
                )
                logger.info(self.report())

            gevent.spawn_later(self.run_time_in_sec, timelimit_stop)

        try:
            logger.info(f"Starting Locust with settings {self.settings.dict()} ")

            self.env = Environment(
                user_classes=self.settings.user_classes,
                host=self.settings.host,
                tags=self.settings.tags,
                exclude_tags=self.settings.exclude_tags,
                reset_stats=self.settings.reset_stats,
                stop_timeout=self.settings.stop_timeout,
            )

            self.env.create_local_runner()
            gevent.spawn(stats_printer(self.env.stats))

            self.env.runner.start(
                user_count=self.settings.num_users, spawn_rate=self.settings.spawn_rate
            )

            self.start_time = time.time()
            self.env.runner.greenlet.join()

        except Exception as e:
            logger.error(f"Locust exception {repr(e)}")

        finally:
            self.env.events.quitting.fire()
