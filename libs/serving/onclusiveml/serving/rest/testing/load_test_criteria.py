# Standard Library
from typing import List, Optional

# Internal libraries
from onclusiveml.serving.rest.testing.load_testing_params import (
    Criterion,
    EnvironmentCriterion,
    EvaluatedCriteria,
    EvaluatedCriterion,
    TestReport,
)


class LoadTestCriteria:
    def __init__(self, criteria: List[Criterion] = []):
        # storage attributes for hard&soft criteria instances
        self.criteria = criteria

        if self.criteria:
            self.n_criteria = len(self.criteria)
        else:
            self.n_criteria = 0

        # storage attribute for the dynamic criterion class definitions
        self.indexed_environment_criteria_classes: List[EnvironmentCriterion] = []

        self.evaluation: Optional[EvaluatedCriteria] = None

    def generate_from_environment(
        self, n_criteria: int = 10
    ) -> List[EnvironmentCriterion]:
        """_summary_

        Returns:
            EnvironmentCriteria: _description_
        """
        # dynamically define subclasses with indexed env prefix
        for criteria_index in range(1, n_criteria + 1):
            # we dynamically subclass, changing only the environment prefix for the fields using
            # the current index as a suffix
            class IndexedEnvironmentCriterion(EnvironmentCriterion):
                """This auto-generated class needs to be instantiated by exporting all of the
                `Criterion`'s class's fields as environment variables with the correct indexed
                prefix. i.e. the following environment variables need to be exported:
                - onclusiveml_serving_criteria_{index}_name
                - onclusiveml_serving_criteria_{index}_threshold
                - onclusiveml_serving_criteria_{index}_ensure_lower
                - onclusiveml_serving_criteria_{index}_endpoint_type
                - onclusiveml_serving_criteria_{index}_endpoint_url

                Args:
                    EnvironmentCriterion (_type_): _description_
                """

                class Config:
                    base_prefix = EnvironmentCriterion.__config__.env_prefix
                    env_prefix = f"{base_prefix}_criteria_{criteria_index}_"
                    env_file_encoding = "utf-8"

            self.indexed_environment_criteria_classes.append(
                IndexedEnvironmentCriterion
            )
        # instantiate all the subclasses and persist the resulting EnvironmnentCriterion-like
        # instances in either the hard or soft criteria attributes for easier test report level
        # evaluation later
        for (
            indexed_environment_criteria_class
        ) in self.indexed_environment_criteria_classes:
            indexed_environment_criteria = indexed_environment_criteria_class()
            self.criteria.append(indexed_environment_criteria)

        self.n_criteria = n_criteria

        # return the populatd attribute

        return self.criteria

    def evaluate(self, test_report: TestReport) -> EvaluatedCriteria:
        """Utility method to verify whether the criteria where met in a load test by comparing the
        threshold(s) against the observed value of the relevant measurement(s), picked out from a
        specified TestReport instance. More specifically:

        - evaluate each listed criterion against the specified test report by calling its
        `was_met_in_report` method.
        - use return to instantiate `EvaluatedCriterion` instances,
        - passes the overall evlaluation if and only if each of the hard-type criteria passes
        - populate the `evaluation` attribute of this instance with a corresponding
            `EvaluatedCriteria` instance

        Args:
            test_report (TestReport): The TestReport instance as returned by a LocusLoadTest's
                `report` method.

        Raises:
            ValueError: If the criteria's endpoint report is available but is missing the criteria's
                measurement, this exeception is raised. This indicates that Locust was able to
                perform a load test successfully, but did not collect the measurement needed to
                evaluate this criteria.

                Note that if the entire endpoint report for the criteria's endpoint id could not be
                found, we return `False`.

        Returns:
            bool: Whether the criteria was met in the specified TestReport.
        """

        evaluated_criteria = []
        hard_criteria_passes = []

        for criterion in self.criteria:
            criterion_passed = criterion.was_met_in_report(test_report)

            evaluated_criterion_kwargs = {
                **{"passed": criterion_passed},
                **criterion.dict(),
            }
            evaluated_criterion = EvaluatedCriterion(**evaluated_criterion_kwargs)
            evaluated_criteria.append(evaluated_criterion)

            if criterion.hard:
                hard_criteria_passes.append(criterion_passed)

        evaluation_pass = all(hard_criteria_passes)

        self.evaluation = EvaluatedCriteria(
            evaluated_criteria=evaluated_criteria, passed=evaluation_pass
        )

        return self.evaluation
