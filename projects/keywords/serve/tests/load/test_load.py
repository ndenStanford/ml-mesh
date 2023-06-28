# 3rd party libraries
from locust import HttpUser, between, task

# Internal libraries
from onclusiveml.serving.rest.testing import (
    Criterion,
    LoadTestingParams,
    LocustLoadTest,
    ValidEndpointTypes,
    ValidMeasurements,
)


class TestWebsiteUser(HttpUser):
    wait_time = between(1, 2)

    @task()
    def get_model_bio(self):
        """
        Gets /
        """
        self.client.get("/v1/model/keywords_model/bio")


model_bio_rps_criterion = Criterion(
    name=ValidMeasurements.requests_rps.value,
    threshold=0.5,
    endpoint_type=ValidEndpointTypes.get.value,
    endpoint_url="/v1/model/keywords_model/bio",
    ensure_lower=False,
)

model_bio_total_reqs_criterion = Criterion(
    name=ValidMeasurements.requests_total.value,
    threshold=4,
    endpoint_type=ValidEndpointTypes.get.value,
    endpoint_url="/v1/model/keywords_model/bio",
    ensure_lower=False,
)


def test_load_model_bio():

    load_test_settings = LoadTestingParams(
        user_classes=[TestWebsiteUser],
        locustfile="",
        host="http://localhost:8000",
        run_time="15s",
        reset_stats=True,
    )

    load_test = LocustLoadTest(settings=load_test_settings)
    load_test.run()
    test_report = load_test.report()

    assert model_bio_rps_criterion.was_met_in_report(test_report)
    assert model_bio_total_reqs_criterion.was_met_in_report(test_report)
