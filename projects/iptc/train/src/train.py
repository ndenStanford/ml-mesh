"""Train IPTC models."""

# Standard Library
import os

# Internal libraries
from onclusiveml.core.logging import get_default_logger


logger = get_default_logger(__name__)

# Source
from src.settings import (  # type: ignore[attr-defined]
    DataFetchParams,
    TrackedIPTCBaseModelCard,
    TrackedIPTCModelSpecs,
)
from src.trainer import IPTCTrainer


def main() -> None:
    """Execute the training process."""
    model_specs = TrackedIPTCModelSpecs()
    model_card = TrackedIPTCBaseModelCard()
    data_fetch_params = DataFetchParams()

    if not os.path.isdir(model_card.local_output_dir):
        os.makedirs(model_card.local_output_dir)
    # Start the training and register models to neptune
    trainer = IPTCTrainer(data_fetch_params, model_card, model_specs)
    trainer()


if __name__ == "__main__":
    main()
