"""Define the IPTC trainer."""

# Standard Library
import os

# ML libs
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    EarlyStoppingCallback,
    Trainer,
)

# 3rd party libraries
from sklearn.model_selection import train_test_split

# Internal libraries
from onclusiveml.data.feature_store import FeatureStoreParams
from onclusiveml.tracking import TrackedModelCard, TrackedModelSpecs
from onclusiveml.training.huggingface.trainer import (
    OnclusiveHuggingfaceModelTrainer,
)

# Source
from src.dataset import IPTCDataset
from src.settings import (  # type: ignore[attr-defined]
    BaseTrackedModelSpecs,
    TrackedIPTCBaseModelCard,
)
from src.utils import compute_metrics


# define the IPTC
tracked_model_specs = BaseTrackedModelSpecs()
model_card = TrackedIPTCBaseModelCard()


# define the IPTC model trainer as a subclass of the OnclusiveHuggingfaceModelTrainer
class IPTCTrainer(OnclusiveHuggingfaceModelTrainer):
    """Class for training and managing Onclusive models."""

    def __init__(
        self,
        tracked_model_specs: TrackedModelSpecs,
        model_card: TrackedModelCard,
        data_fetch_params: FeatureStoreParams,
    ) -> None:
        """Initialize the OnclusiveModelTrainer.

        Args:
            tracked_model_specs (TrackedModelSpecs): Specifications for tracked model on neptune.
            model_card (TrackedModelCard): Model card with specifications of the model.
            data_fetch_params (FeatureStoreParams): Parameters for fetching data from feature store.

        Returns: None
        """
        super().__init__(
            tracked_model_specs=tracked_model_specs,
            model_card=model_card,
            data_fetch_params=data_fetch_params,
        )

    def initialize_model(self) -> None:
        """Initialize model and tokenizer."""
        model_name = model_card.model_name
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def create_training_argument(self) -> None:
        """Create training argument object for Huggingface trainer."""
        self.training_args = TrackedIPTCBaseModelCard(
            num_train_epochs=self.model_card.epochs,
            learning_rate=self.model_card.learning_rate,
            report_to=self.model_card.report_to,
            compute_metrics=compute_metrics,
            model_name=self.model_card.model_name,
            save_steps=self.model_card.save_steps,
            save_total_limit=self.model_card.save_total_limit,
            early_stopping_patience=self.model_card.early_stopping_patience,
        )

    def data_preprocess(self) -> None:
        """Preprocess to torch dataset and split for train and evaluation."""
        self.train_df, self.eval_df = train_test_split(
            self.dataset_df,
            test_size=0.20,
            stratify=self.dataset_df[f"topic_{self.model_card.level}"],
        )
        self.train_dataset = IPTCDataset(
            self.train_df,
            self.model_card.tokenizer,
            self.model_card.level,
            self.model_card.selected_text,
            self.model_card.first_level_root,
            self.model_card.second_level_root,
        )
        self.eval_dataset = IPTCDataset(
            self.eval_df,
            self.model_card.tokenizer,
            self.model_card.level,
            self.model_card.selected_text,
            self.model_card.first_level_root,
            self.model_card.second_level_root,
        )

    def train(self) -> None:
        """Train the model."""
        # using this class directly should give us tracking capability
        # https://docs.neptune.ai/integrations/transformers/
        self.trainer = Trainer(
            model=self.model,
            args=self.training_args,
            train_dataset=self.train_dataset,
            eval_dataset=self.eval_dataset,
            tokenizer=self.tokenizer,
            callbacks=[
                EarlyStoppingCallback(
                    early_stopping_patience=self.model_card.early_stopping_patience
                )
            ],
        )
        self.trainer.train()

    def predict(self, inputs: str):  # type: ignore[no-untyped-def]
        """Implement prediction logic."""
        prediction = self.trainer.predict(inputs)
        return prediction

    def save(self) -> None:
        """Save the model."""
        self.iptc_model_local_dir = os.path.join(
            self.model_card.local_output_dir, f"{self.model_card.model_params.with_id}"
        )
        self.trainer.save_model(
            self.iptc_model_local_dir, serialization="pytorch", save_ctfidf=True
        )

    def __call__(self) -> None:
        """Call Method."""
        super(OnclusiveHuggingfaceModelTrainer, self).__call__()
        self.logger.info(
            f"Training data uploaded to s3 location : {self.full_file_key}"
        )
        self.initialize_model()
        self.optimize_model()
        self.save()
        if self.data_fetch_params.save_artifact:
            sample_docs = self.model_card.sample_documents
            sample_predictions = self.predict(sample_docs)

        super(OnclusiveHuggingfaceModelTrainer, self).__call__(
            [sample_docs, self.model_card.model_params.dict(), sample_predictions],
            [
                self.model_card.model_test_files.inputs,
                self.model_card.model_test_files.inference_params,
                self.model_card.model_test_files.predictions,
            ],
            self.iptc_model_local_dir,
        )
