# Standard Library
import json

# Internal libraries
from onclusiveml.serving.rest.testing import LoadTest, LoadTestCriteria


def test_load_model(test_load_test_settings, test_model_criteria):
    # run load test
    load_test = LoadTest(settings=test_load_test_settings)
    load_test.run()
    # get load test report
    test_report = load_test.report()
    # export test report
    with open("load_test_report.json", "w") as report_file:
        json.dump(test_report.dict(), report_file)
    # initialize load test criteria
    load_test_criteria = LoadTestCriteria(criteria=test_model_criteria)
    # evaluate load test criteria
    test_evaluation = load_test_criteria.evaluate(test_report)
    # export test report
    with open("load_test_evaluation.json", "w") as evaluation_file:
        json.dump(test_evaluation.dict(), evaluation_file)

    load_test_result_actual = load_test_criteria.evaluation.passed

    assert load_test_result_actual
