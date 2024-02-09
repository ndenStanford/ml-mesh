"""Register trained model."""

# Standard Library
import os

# Internal libraries
from onclusiveml.core.logging import get_default_logger
from onclusiveml.nlp.stopwords.helpers import load_stop_words_file
from onclusiveml.train import BertopicTrainer

# Source
from src.settings import (  # type: ignore[attr-defined]
    DataFetchParams,
    TrackedTopicBaseModelCard,
    TrackedTopicModelSpecs,
)


logger = get_default_logger(__name__)


def main() -> None:
    """Register trained model."""
    model_specs = TrackedTopicModelSpecs()
    model_card = TrackedTopicBaseModelCard()
    data_fetch_params = DataFetchParams()

    if not os.path.isdir(model_card.local_output_dir):
        os.makedirs(model_card.local_output_dir)

    stopwords = load_stop_words_file(lang=model_card.model_params.stop_words_lang)

    bertopic_trainer = BertopicTrainer(
        tracked_model_specs=model_specs,
        model_card=model_card,
        data_fetch_params=data_fetch_params,
        stopwords=stopwords,
    )

    bertopic_trainer()


if __name__ == "__main__":
    main()
