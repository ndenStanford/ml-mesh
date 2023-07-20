# 3rd party libraries
import pytest
from locust import HttpUser, between, task

# Internal libraries
from libs.serving.onclusiveml.serving.rest.testing.load_test import (
    LoadTest,
    LoadTestingParams,
    TestReport,
)


class TestWebsiteUser(HttpUser):
    wait_time = between(1, 2)

    @task()
    def get_home_page(self):
        """
        Gets /
        """
        self.client.get("/")


@pytest.mark.parametrize(
    "test_user_classes",
    [
        [TestWebsiteUser],  # configure test using user classes
        [],  # configure test using locustfile
    ],
)
def test_locus_load_test_run_and_report(test_user_classes, test_locustfile):
    """Tests the running and reporting methods of the LoadTest class by running a genuine load test
    against http://github.com and producing a report."""

    if test_user_classes:
        test_locustfile = ""

    load_test_settings = LoadTestingParams(
        user_classes=test_user_classes,
        locustfile=test_locustfile,
        host="http://github.com",
        run_time="15s",
        reset_stats=True,
    )

    load_test = LoadTest(settings=load_test_settings)
    load_test.run()
    test_report = load_test.report()

    assert isinstance(test_report, TestReport)
