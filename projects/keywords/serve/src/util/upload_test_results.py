# Standard Library
import os

# Internal libraries
from onclusiveml.tracking import (
    TrackedGithubActionsSpecs,
    TrackedImageSpecs,
    TrackedModelVersion,
)

# Source
from src.params import ServedModelParams
from src.util.params import TrackedCompiledModelSpecs


def main() -> None:

    # model registry reference to the desired (compiled) model version
    model_version_specs = TrackedCompiledModelSpecs()
    # output directory specs
    model_export_params = ServedModelParams()
    # initialize client for specific model version
    mv = TrackedModelVersion(**model_version_specs.dict())

    docker_image_specs = TrackedImageSpecs()

    test_results_neptune_attribute_path = (
        f"model/test_results/{docker_image_specs.docker_image_tag}"
    )
    # upload the test report .json
    mv.upload_file_to_model_version(
        neptune_attribute_path=f"{test_results_neptune_attribute_path}/load_test_report.json",
        local_file_path=os.path.join(
            model_export_params.model_directory, "load_test_report.json"
        ),
        use_s3=False,
    )
    # upload the criteria evaluation .json
    mv.upload_file_to_model_version(
        neptune_attribute_path=f"{test_results_neptune_attribute_path}/load_test_evaluation.json",
        local_file_path=os.path.join(
            model_export_params.model_directory, "load_test_evaluation.json"
        ),
        use_s3=False,
    )
    # upload the github action specs .json
    github_action_specs = TrackedGithubActionsSpecs()

    mv.upload_config_to_model_version(
        config=github_action_specs.dict(),
        neptune_attribute_path=f"{test_results_neptune_attribute_path}/github_action_context.json",
    )
    # upload the docker image specs .json
    mv.upload_config_to_model_version(
        config=docker_image_specs.dict(),
        neptune_attribute_path=f"{test_results_neptune_attribute_path}/serve_image_specs.json",
    )
    # shutdown client
    mv.stop()


if __name__ == "__main__":

    main()
