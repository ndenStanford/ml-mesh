# Internal libraries
from onclusiveml.serving.rest.testing import (
    Criterion,
    LoadTestCriteria,
    ValidEndpointTypes,
    ValidMeasurements,
)


def test_load_test_criteria():

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

    LoadTestCriteria(criteria=test_criteria)


def test_load_test_criteria_evaluate():

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

    LoadTestCriteria(criteria=test_criteria)
