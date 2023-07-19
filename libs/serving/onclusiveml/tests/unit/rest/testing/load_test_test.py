# 3rd party libraries
from locust import HttpUser

# Internal libraries
from onclusiveml.serving.rest.testing import LoadTest, LoadTestingParams


def test_load_test():
    """Tests the initialization of a LoadTest instance"""

    test_settings = LoadTestingParams(user_classes=[HttpUser], locustfile="")

    test_load_test = LoadTest(settings=test_settings)

    assert test_load_test.settings == test_settings
    assert test_load_test.start_time == -1
    assert test_load_test.end_time == -1
