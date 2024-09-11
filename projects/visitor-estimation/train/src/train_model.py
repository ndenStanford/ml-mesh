"""Train IPTC model."""

# Standard Library
import os

# Internal libraries
from onclusiveml.core.logging import get_default_logger

# Source
from src.settings import (  # type: ignore[attr-defined]
    DataFetchParams,
    TrackedVEBaseModelCard,
    TrackedVEModelSpecs,
)

from src.trainer import VisitorEstimationTrainer

logger = get_default_logger(__name__)


def main() -> None:
    """Execute the training process."""
    data_fetch_params = DataFetchParams()
    model_specs = TrackedVEModelSpecs()
    model_card = TrackedVEBaseModelCard()

    # Start the training and register models to neptune
    trainer = VisitorEstimationTrainer(model_specs, model_card, data_fetch_params)
    trainer()


if __name__ == "__main__":
    main()
