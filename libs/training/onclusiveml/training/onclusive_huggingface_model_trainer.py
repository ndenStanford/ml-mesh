"""Class for training and managing Onclusive models."""

# Standard Library
from abc import abstractmethod

# ML libs
from transformers import EarlyStoppingCallback, Trainer

# Internal libraries
from onclusiveml.data.feature_store import FeatureStoreParams
from onclusiveml.tracking import TrackedModelCard, TrackedModelSpecs
from onclusiveml.training.onclusive_model_trainer import OnclusiveModelTrainer


class OnclusiveHuggingfaceModelTrainer(OnclusiveModelTrainer):
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

    @abstractmethod
    def initialize_model(self) -> None:
        """Initialize modell and tokenizer.

        Example implementation
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        """
        pass

    @abstractmethod
    def create_training_argument(self) -> None:
        """Create training argument object for Huggingface trainer.

        Example implementation
        self.training_args = TrainingArguments(
          output_dir=self.model_cardoutput_dir,
          num_train_epochs=self.model_cardepochs,
          learning_rate=self.model_card.learning_rate
        )
        """
        pass

    def train(self) -> None:
        """Train the model.

        Returns: None
        """
        # using this class directly should give us tracking capability
        # https://docs.neptune.ai/integrations/transformers/
        self.trainer = Trainer(
            model=self.model,
            args=self.training_args,
            train_dataset=self.docs,
            tokenizer=self.tokenizer,
            callbacks=[EarlyStoppingCallback(early_stopping_patience=1)],
        )
        self.trainer.train()
        return

    @abstractmethod
    def predict(self) -> None:
        """Make predictions using the trained model.

        Returns: None
        """
        pass

    def optimize_model(self) -> None:
        """Optimize the model.

        Returns: None
        """
        self.train()

    def __call__(self) -> None:
        """Call Method."""
        super(OnclusiveHuggingfaceModelTrainer, self).__call__()
        self.logger.info(
            f"Training data uploaded to s3 location : {self.full_file_key}"
        )
        self.initialize_model()
        self.optimize_model()
        self.save()
