"""Pipeline test."""

# 3rd party libraries
import pytest
from apache_beam.testing.test_pipeline import TestPipeline

# Source
from src.backfill.pipeline import get_pipeline
from src.settings import get_settings


# NOTE: until we have a reliable way to mock the kafka consumer
# this is the behaviour consistency we can keep testing for.
@pytest.mark.xfail(raises=RuntimeError)
def test_pipeline():
    """Test enrichment pipeline."""
    with TestPipeline() as pipeline:
        _ = get_pipeline(pipeline, get_settings())
        pipeline.run()
