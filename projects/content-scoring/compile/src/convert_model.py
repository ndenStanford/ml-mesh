"""Compile model."""

# Standard Library
from typing import Any, Dict  # noqa

# ML libs
import torch  # noqa

# 3rd party libraries
import joblib
from hummingbird.ml import convert

# Internal libraries
from onclusiveml.core.logging import (
    OnclusiveLogMessageFormat,
    get_default_logger,
)
from onclusiveml.tracking import TrackedModelVersion

# Source
from src.settings import (  # type: ignore[attr-defined]
    IOSettings,
    UncompiledTrackedModelSpecs,
)


def main() -> None:
    """Compile model."""
    io_settings = IOSettings()
    logger = get_default_logger(
        name=__name__,
        fmt_level=OnclusiveLogMessageFormat.DETAILED.name,
        level=io_settings.log_level,
    )
    # get read-only base model version
    base_model_specs = UncompiledTrackedModelSpecs()
    base_model_version = TrackedModelVersion(**base_model_specs.dict())
    # get base model
    base_model: Any = base_model_version.download_file_from_model_version(  # noqa
        local_file_path="src/model/model.pkl",  # noqa
        neptune_attribute_path="model/model_artifacts",  # noqa
    )  # noqa
    model = joblib.load("src/model/model.pkl")
    # compile base model pipeline for iptc
    converted_model = convert(model, "torch")

    converted_model.save_pretrained(io_settings.compile.model_directory)

    logger.debug(
        f"Successfully exported compiled content_scoring model to: {io_settings.compile.model_directory}"  # noqa
    )


if __name__ == "__main__":
    main()
