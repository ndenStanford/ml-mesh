"""Compile model."""

# Standard Library
from typing import Any, Dict  # noqa

# ML libs
import torch  # noqa

# 3rd party libraries
import joblib
from hummingbird.ml import convert

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSettings
from onclusiveml.core.logging import get_default_logger
from onclusiveml.tracking import TrackedModelSettings, TrackedModelVersion

# Source
from src.settings import get_settings


def compile(settings: OnclusiveBaseSettings) -> None:
    """Compile model."""
    logger = get_default_logger(
        name=__name__,
        fmt_level=settings.fmt_level,
        level=settings.level,
        json_format=settings.json_format,
    )

    # get read-only base model version
    base_model_specs = TrackedModelSettings()
    base_model_version = TrackedModelVersion(**base_model_specs.model_dump())

    base_model_card: Dict = (  # noqa
        base_model_version.download_config_from_model_version(  # noqa
            "model/model_card"  # noqa
        )
    )  # noqa

    model_pipeline_base = joblib.load(settings.download.model_base)
    # compile base model pipeline for content-scoring
    converted_model = convert(model_pipeline_base, "torch")

    torch.save(converted_model, settings.compile.compiled_model_base)

    logger.debug(
        f"Successfully exported compiled content_scoring model to: {settings.compile.model_directory}"  # noqa
    )


if __name__ == "__main__":
    compile(get_settings())
