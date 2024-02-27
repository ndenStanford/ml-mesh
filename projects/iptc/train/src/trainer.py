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

# Internal libraries
from onclusiveml.training.huggingface.trainer import (
    OnclusiveHuggingfaceModelTrainer,
)

# Source
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

    def __init__(  # type: ignore[no-untyped-def]
        self, train_dataset, eval_dataset, tracked_model_specs, model_card
    ):
        super().__init__(train_dataset, eval_dataset, tracked_model_specs, model_card)
        # Implement any additional initialization if needed

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
            training_filename=self.model_card.training_filename,
            test_filename=self.model_card.test_filename,
            save_steps=self.model_card.save_steps,
            save_total_limit=self.model_card.save_total_limit,
            early_stopping_patience=self.model_card.early_stopping_patience,
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

    def predict(self):  # type: ignore[no-untyped-def]
        """Implement prediction logic."""
        sample_prediction = self.trainer.predict(
            self.model_card.model_inputs.sample_documents
        )
        return sample_prediction

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
