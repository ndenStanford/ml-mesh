"""Register trained model."""

# Standard Library
import os

# Internal libraries
from onclusiveml.core.logging import get_default_logger
from onclusiveml.nlp.stopwords.helpers import load_stop_words_file
from onclusiveml.training import BertopicTrainer

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

    data_fetch_configurations = {
        "entity_df": """ SELECT iptc_id, CURRENT_TIMESTAMP AS event_timestamp FROM "features"."pred_iptc_first_level" """,
        "features": [
            "topic_feature_view:topic_1",
            "topic_feature_view:content",
            "topic_feature_view:title",
            "topic_feature_view:language",
        ],
    }

    data_fetch_params.entity_df = data_fetch_configurations["entity_df"]
    data_fetch_params.features = data_fetch_configurations["features"]

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
