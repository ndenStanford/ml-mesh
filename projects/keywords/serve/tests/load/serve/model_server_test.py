"""Load test."""

# Standard Library
import json
import os

# Internal libraries
from onclusiveml.serving.rest.testing.load_test import (
    LoadTest,
    LoadTestCriteria,
)

# Source
from src.params import ServedModelParams


def test_load_model(test_load_test_settings, test_model_criteria):
    """Runs load test."""
    # --- run load test
    # run load test
    load_test = LoadTest(settings=test_load_test_settings)
    load_test.run()
    # get load test report
    test_report = load_test.report()
    # export test report
    model_export_params = ServedModelParams()

    load_test_report_export_path = os.path.join(
        model_export_params.model_directory, "load_test_report.json"
    )

    with open(load_test_report_export_path, "w") as report_file:
        json.dump(test_report.model_dump(), report_file)
    # --- evaluate load test
    # initialize load test criteria
    load_test_criteria = LoadTestCriteria(criteria=test_model_criteria)
    # evaluate load test criteria
    test_evaluation = load_test_criteria.evaluate(test_report)
    # export evaluation results
    load_test_evaluation_export_path = os.path.join(
        model_export_params.model_directory, "load_test_evaluation.json"
    )

    with open(load_test_evaluation_export_path, "w") as evaluation_file:
        json.dump(test_evaluation.model_dump(), evaluation_file)
    # pass/fail
    load_test_result_actual = load_test_criteria.evaluation.passed

    assert load_test_result_actual
