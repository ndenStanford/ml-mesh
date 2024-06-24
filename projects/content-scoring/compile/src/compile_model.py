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
    UncompiledTrackedModelSettings,
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
    base_model_specs = UncompiledTrackedModelSettings()
    base_model_version = TrackedModelVersion(**base_model_specs.model_dump())

    base_model_card: Dict = (  # noqa
        base_model_version.download_config_from_model_version(  # noqa
            "model/model_card"  # noqa
        )
    )  # noqa

    model_pipeline_base = joblib.load(io_settings.download.model_base)
    # compile base model pipeline for content-scoring
    converted_model = convert(model_pipeline_base, "torch")

    torch.save(converted_model, io_settings.compile.compiled_model_base)

    logger.debug(
        f"Successfully exported compiled content_scoring model to: {io_settings.compile.model_directory}"  # noqa
    )


if __name__ == "__main__":
    main()
