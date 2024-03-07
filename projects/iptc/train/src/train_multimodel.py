"""Train multiple IPTC models."""

# Standard Library
import os

# Internal libraries
from onclusiveml.core.logging import get_default_logger

# Source
from src.settings import (  # type: ignore[attr-defined]
    DataFetchParams,
    TrackedIPTCBaseModelCard,
    TrackedIPTCMultiModelSpecs,
    TrackedModelSpecs,
)
from src.trainer import IPTCTrainer


logger = get_default_logger(__name__)


def main() -> None:
    """Execute the multimodel training process."""
    data_fetch_params = DataFetchParams()
    multimodel_specs = TrackedIPTCMultiModelSpecs()
    for project, model_name in zip(multimodel_specs.project, multimodel_specs.model):
        model_specs = TrackedModelSpecs(project=project, model_name=model_name)
        model_card = TrackedIPTCBaseModelCard(model_name=model_name)

        if not os.path.isdir(model_card.local_output_dir):
            os.makedirs(model_card.local_output_dir)
        # Start the training and register models to neptune
        trainer = IPTCTrainer(data_fetch_params, model_card, model_specs)
        trainer()


if __name__ == "__main__":
    main()
