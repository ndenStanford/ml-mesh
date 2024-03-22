"""Main pipeline."""

# Standard Library
import logging

# 3rd party libraries
import apache_beam as beam

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSettings
from onclusiveml.core.base.pydantic import cast
from onclusiveml.data.beam.settings import PipelineSettings

# Source
from src.backfill.pipeline import get_pipeline
from src.settings import get_settings


def run_beam_pipeline(settings: OnclusiveBaseSettings) -> None:
    """Runs beam pipeline."""
    logging.getLogger().setLevel(logging.INFO)

    flink_options = cast(settings, PipelineSettings).to_pipeline_options()

    with beam.Pipeline(options=flink_options) as pipeline:
        _ = get_pipeline(pipeline, settings)

        result = pipeline.run()
        result.wait_until_finish()

    logging.info("Pipeline execution completed.")


if __name__ == "__main__":
    run_beam_pipeline(get_settings())
