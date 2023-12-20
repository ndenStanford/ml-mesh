"""Upload test results."""

# Standard Library
import os

# Internal libraries
from onclusiveml.core.base.pydantic import cast
from onclusiveml.tracking import (
    TrackedGithubActionsSpecs,
    TrackedImageSpecs,
    TrackedModelVersion,
)

# Source
from src.settings import (  # type: ignore[attr-defined]
    GlobalSettings,
    TrackedCompiledModelSpecs,
    get_settings,
)


settings = get_settings()


def main(settings: GlobalSettings) -> None:
    """Upload test results."""
    # model registry reference to the desired (compiled) model version)
    github_action_specs = cast(settings, TrackedGithubActionsSpecs)
    model_version_specs = cast(settings, TrackedCompiledModelSpecs)
    docker_image_specs = cast(settings, TrackedImageSpecs)
    # initialize client for specific model version
    mv = TrackedModelVersion(**model_version_specs.dict())

    test_results_neptune_attribute_path = (
        f"model/test_results/{settings.docker_image_tag}"
    )
    # upload the test report .json
    mv.upload_file_to_model_version(
        neptune_attribute_path=f"{test_results_neptune_attribute_path}/load_test_report.json",
        local_file_path=os.path.join(settings.model_directory, "load_test_report.json"),
        use_s3=False,
    )
    # upload the criteria evaluation .json
    mv.upload_file_to_model_version(
        neptune_attribute_path=f"{test_results_neptune_attribute_path}/load_test_evaluation.json",
        local_file_path=os.path.join(
            settings.model_directory, "load_test_evaluation.json"
        ),
        use_s3=False,
    )

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
    main(settings)
