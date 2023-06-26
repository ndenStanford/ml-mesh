# 3rd party libraries
import pytest
from locust import HttpUser, between, task

# Internal libraries
from onclusiveml.serving.rest.testing import LoadTestingParams, LocustLoadTest


class TestWebsiteUser(HttpUser):
    wait_time = between(1, 2)

    @task()
    def get_home_page(self):
        """
        Gets /
        """
        self.client.get("/")


@pytest.mark.parametrize(
    "test_user_classes, test_locustfile",
    [
        ([TestWebsiteUser], ""),  # configure test using user classes
        (
            [],
            "libs/serving/onclusiveml/tests/integration/rest/testing/test_locustfile.py",
        ),  # configure test using locustfile
    ],
)
def test_locus_load_test(test_user_classes, test_locustfile):

    load_test_settings = LoadTestingParams(
        user_classes=test_user_classes,
        locustfile=test_locustfile,
        host="http://github.com",
        run_time="15s",
        reset_stats=True,
    )

    load_test = LocustLoadTest(settings=load_test_settings)
    load_test.run()
    test_report = load_test.report()

    assert test_report.num_requests > 5
    assert test_report.end_time > test_report.start_time
    assert test_report.completed["GET_/"].endpoint_id == "GET_/"
    assert test_report.completed["GET_/"].measurements.requests_total.value > 0
    assert test_report.completed["GET_/"].measurements.failures_total.value < 3
    assert test_report.completed["GET_/"].measurements.failures_percent.value < 0.5
