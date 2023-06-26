# 3rd party libraries
import pytest
from locust import HttpUser, between, task

# Internal libraries
from onclusiveml.serving.rest.testing import LoadTestingParams, LocustLoadTest


class TestWebsiteUser(HttpUser):
    wait_time = between(1, 3)

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
        host="https://github.com",
        run_time="15s",
    )

    load_test = LocustLoadTest(settings=load_test_settings)
    load_test.run()
    stats = load_test.stats()

    assert stats["num_requests"] > 5
    assert stats["end_time"] > stats["start_time"]
    assert stats["requests"]["GET_/"]["total_rpm"] > 0
