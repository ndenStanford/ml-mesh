# Standard Library
from typing import List, Optional

# Internal libraries
from onclusiveml.serving.rest.testing.load_test.params import (
    Criterion,
    EnvironmentCriteriaCount,
    EnvironmentCriterion,
    EvaluatedCriteria,
    EvaluatedCriterion,
    TestReport,
)


class LoadTestCriteria(object):
    """A utility class to
    - provide `Criteria` instances either through
        - direct specification via the constructor argument, or
        - dynamic definition and creation, using exclusively indexed environment variables to set
            the fields' values - see `generate_from_environment`
    - evaluate `Criteria` instances against a `TestReport` instance, and collecting the individual
        fail/pass results into one final fail/pass, taking into account the `hard` attribute of each
        `Criteria` instance

    The list of `Criteria` instances stored in the `criteria` attribute together define the profile
    of a `LoadTest` level criterion. If and only if all `hard` type criteria in that list pass
    individually, will the overall evaluation pass. See also the method `evaluate`.
    """

    def __init__(self, criteria: List[Criterion] = []):
        """Constructor of the class. A list of

        Args:
            criteria (List[Criterion], optional): The criteria that define the `LoadTest` level
                performance requirements. Defaults to []. Populates the `criteria` attribute.
                If not specified, the `criteria` attribute can be set via the
                `generate_from_environment` method.
        """
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
        self, n_criteria: Optional[int] = None
    ) -> List[EnvironmentCriterion]:
        """A utility method to dynamically define and create a list of `EnvironmentCriteria`
        instances sourced exclusively from the corresponding environment variables. The resulting
        list of `Criteria` instances will populate the `criteria` attribute.

        More specifically: For each index 1,...,n_criteria:
        - the following environment variables need to be exported with the correct values:
            - onclusiveml_serving_criteria_{index}_name
            - onclusiveml_serving_criteria_{index}_threshold
            - onclusiveml_serving_criteria_{index}_ensure_lower
            - onclusiveml_serving_criteria_{index}_endpoint_type
            - onclusiveml_serving_criteria_{index}_endpoint_url
        - an `EnvironmentCriteria` subclass will be defined, with the only difference being the
            environment variable prefix being extended by `criteria_{index}_`
        - an instance of the above subclass will be instantiated, assuming the above environment
            variables have been export correctly

        This is useful in CI settings, were entire `LoadTest` performance profiles can now be
        configured using environment variables.

        Args:
            n_criteria (int, optional): The number of environment criteria to generate. If not
                specified, attempts to obtain the value from reading the corresponding environment
                variable from the `EnvironmentCriteriaCount` class' `n_criteria` field.

        Returns:
            List[EnvironmentCriterion]: A list of `EnvironmentCriterion` instances definine the
            `LoadTest` level performance requirements
        """
        # if the number of criteria is not specified in function call, obtain it from environment
        if n_criteria is None:
            n_criteria = EnvironmentCriteriaCount().n_criteria
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
                """

                class Config:
                    base_prefix = EnvironmentCriterion.__config__.env_prefix
                    env_prefix = f"{base_prefix}criteria_{criteria_index}_"
                    env_file_encoding = "utf-8"

            self.indexed_environment_criteria_classes.append(
                IndexedEnvironmentCriterion
            )
        # instantiate all the subclasses and persist the resulting EnvironmnentCriterion instances
        for (
            indexed_environment_criteria_class
        ) in self.indexed_environment_criteria_classes:
            indexed_environment_criteria = indexed_environment_criteria_class()
            self.criteria.append(indexed_environment_criteria)

        self.n_criteria = n_criteria
        # return the populatd attribute
        return self.criteria

    def evaluate(self, test_report: TestReport) -> EvaluatedCriteria:
        """Utility method to verify whether
            - the individual `Criterion`/`EnvironmentCriterion` instances in the `criteria`
                attribute where met in a load test by comparing the threshold(s) against the
                observed value of the relevant measurement(s), picked out from a specified
                TestReport instance, by calling the criterion's `was_met_in_report` method
            - the overall evaluation has passed, based on the above individual outcomes. The overall
                evaluation is considered a pass if and only if all the `hard` type `Criterion`
                instances in the `criteria` attribute return a successful pass result from their
                respective `was_met_in_report` method calls against the `test_report`.
            - return an `EvaluatedCriteria` instance that captures:
                - the individual `Criterion`s/`EnvironmentCriterion`s specs
                - all the individual `Criterion`s/`EnvironmentCriterion`s evluation outcomes
                - the overall evaluation outcome

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
            EvaluatedCriteria: The outcome of the evaluation of the load test performance
                requirements against the load test report.
        """

        evaluated_criteria = []
        hard_criteria_passes = []

        for criterion in self.criteria:
            # evaluate criterion on report
            criterion_passed = criterion.was_met_in_report(test_report)
            # generate evaluated criterion for the original criterion and its evaluation & persist
            evaluated_criterion_kwargs = {
                **{"passed": criterion_passed},
                **criterion.dict(),
            }
            evaluated_criterion = EvaluatedCriterion(**evaluated_criterion_kwargs)
            evaluated_criteria.append(evaluated_criterion)
            # keep track of the hard criterion evaluation outcomes - they are what drives the
            # overall load test performance pass/fail
            if criterion.hard:
                hard_criteria_passes.append(criterion_passed)
        # evaluate the load test as a whole
        evaluation_pass = all(hard_criteria_passes)
        # assemble the evaluated criteria instance, capturing
        # - the individual `Criterion`s/`EnvironmentCriterion`s specs
        # - all the individual `Criterion`s/`EnvironmentCriterion`s evluation outcomes
        # - the overall evaluation outcome
        self.evaluation = EvaluatedCriteria(
            evaluated_criteria=evaluated_criteria, passed=evaluation_pass
        )

        return self.evaluation
