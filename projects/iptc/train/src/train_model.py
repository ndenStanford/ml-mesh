"""Train IPTC model."""

# Standard Library
import os

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
    trainer = IPTCTrainer(model_specs, model_card, data_fetch_params)
    trainer()


if __name__ == "__main__":
    main()
